import polars as pl
import re
from geopy.geocoders import Nominatim
import math
import csv
from urllib.parse import urlparse, urlencode
import json
import time

from logger import logger_setup
import openai, os

from config import NOT_FOUND, BBOXES_CSV, AIRPORT_CODES_CSV, CITIES_COUNTRIES_CSV
from config import EURO_ZONE, EURO_ZONE_LOWEST_PRICE, EURO_ZONE_DURATION_LIMIT
from config import OUTPUT_CSV_DIR, INNER_JSON_DIR


logger = logger_setup()

# set up all dataframes
df_bb = pl.read_csv(BBOXES_CSV)
df_airports = pl.read_csv(AIRPORT_CODES_CSV)
df_cities_countries = pl.read_csv(CITIES_COUNTRIES_CSV)

   
def get_cities():
    return sorted(df_cities_countries['city'])

   
def get_city_name(id):
    return df_cities_countries.filter(pl.col('id_city') == id)['city'][0]
    
    
def get_city_id(name):
    try:
        return df_cities_countries.filter(pl.col('city') == name)['id_city'][0]
    except:
        return NOT_FOUND


def get_modify_url(url: str, params: dict):
    
    url = url.replace('#/search', 'search')
    
    # Parse the URL into its component parts
    parsed_url = urlparse(url)
    #print(parsed_url)

    # Get the query string parameters as a dictionary
    query_params = dict([qp.split('=') for qp in parsed_url.query.split('&')])
    #print(query_params)

    # Replace the values of any parameters specified in the params dictionary
    for key, value in params.items():
        if key in query_params:
            query_params[key] = value

    # Encode the modified query parameters and rebuild the URL
    new_query_string = urlencode(query_params)
    new_url = parsed_url._replace(query=new_query_string).geturl()

    new_url = new_url.replace('search', '#/search')
    
    return new_url
    
    
def get_bboxes(city_country):
    geolocator = Nominatim(user_agent='terraqwerty')
    
    try:          
        location = geolocator.geocode(', '.join(city_country))
                
        bbox = list(map(lambda x: round(float(x), 4), list(filter(lambda x: x[0] == 'boundingbox', location.raw.items()))[0][1]))
        lat_min, lat_max, lon_min, lon_max = bbox
        
        lat = round(float(list(filter(lambda x: x[0] == 'lat', location.raw.items()))[0][1]), 4)
        lon = round(float(list(filter(lambda x: x[0] == 'lon', location.raw.items()))[0][1]), 4)
        
        if (lat_min <= lat <= lat_max) and (lon_min <= lon <= lon_max):
            return bbox, [lat, lon] 
        
        return None
        
    except AttributeError as err:
        print(city_country, err)
            
            
# attempt to catch the bus or train stations at the airports by station name       
def get_id_by_station_name(station_name: str) -> int:
    try:
        station_name = station_name.replace(',', ' ').split()
        id = list(filter(lambda x: len(x) != 0, 
                    map(lambda x: df_cities_countries.filter(pl.col('city') == x)['id_city'], station_name)))
        return id[0][0] 
    except:
        return NOT_FOUND


# attempt to catch the bus or train stations at the airports by airport code
def get_id_by_station_acode(station_name: str) -> int:
    try:
        station_name = station_name.replace(',', ' ').split()  
        id = list(filter(lambda x: x != NOT_FOUND, 
                    map(get_id_from_acode, 
                    filter(lambda x: re.fullmatch('[a-z|A-Z]{3}', x) != None, station_name))))
        return id[0]
    except:
        return NOT_FOUND
        
        
# seeks for city id by the given coordinates
def get_id_from_bb(coords: list) -> int:
    try:       
        in_lat = (df_bb['lat_min'] <= coords[0]) & (df_bb['lat_max'] >= coords[0])
        in_lon = (df_bb['lon_min'] <= coords[1]) & (df_bb['lon_max'] >= coords[1])
        
        id = df_bb.filter(in_lat & in_lon)['id_city']        
    
        return id[0]
        
    except:
        return NOT_FOUND    


# seeks for city id by airport code like 'THR', 'AUB', 'GKO' etc.
def get_id_from_acode(code: str) -> int:
    try:
        id = df_airports.filter(df_airports['code'] == code.lower())['id_city']
        
        return id[0]
    
    except:
        return NOT_FOUND  


# compare actual price to predict one
def price_to_predict(from_id: int, to_id: int, price: int, duration: int, ttype: str, path_id: int) -> int:
    if (from_id in EURO_ZONE and to_id in EURO_ZONE):
        #K_1, K_2, Q = 0.5385133730326261, 0.10985332568233755, 0.3
        #predicted_price = 10**(K_1)*duration**(K_2)
        K_1, K_2, Q = -2.2022, 0.8832, {'bus': 0.12, 'share': 0.25}
        predict = math.exp(K_1 + K_2 * math.log(duration))
        low_limit = math.ceil((1 - Q[ttype]) * predict)
        
        if price < low_limit:            
            
            from_city = df_cities_countries.filter(pl.col('id_city') == from_id)['city'][0]
            to_city = df_cities_countries.filter(pl.col('id_city') == to_id)['city'][0]
            
            with open(OUTPUT_CSV_DIR/'lower_predict.csv', 'a') as csvfile:
                # Create a writer object
                writer = csv.writer(csvfile)
                
                # Write the header row if the file is empty
                if csvfile.tell() == 0:
                    writer.writerow(('path_id','from_id','to_id','from','to','transport','duration','price','low_limit','predict'))
                
                # Write the record to the file
                writer.writerow((path_id,from_id,to_id,from_city,to_city,ttype,duration,price,low_limit,round(predict, 1)))
            
            price = low_limit # price changing                   
            
    return price


# check the minimal euro zone conditions
def price_to_eu_terms(from_id: int, to_id: int, price: int, duration: int, ttype: str, path_id) -> int:
    if (from_id in EURO_ZONE and to_id in EURO_ZONE):
        if price < EURO_ZONE_LOWEST_PRICE and duration > EURO_ZONE_DURATION_LIMIT:

            from_city = df_cities_countries.filter(pl.col('id_city') == from_id)['city'][0]
            to_city = df_cities_countries.filter(pl.col('id_city') == to_id)['city'][0]
            
            with open(OUTPUT_CSV_DIR/'lower_5-60.csv', 'a') as csvfile:
                # Create a writer object
                writer = csv.writer(csvfile)
                
                # Write the header row if the file is empty
                if csvfile.tell() == 0:
                    writer.writerow(('path_id','from_id','to_id','from','to','transport','duration','price','eu_lowest_price'))
                
                # Write the record to the file
                writer.writerow((path_id,from_id,to_id,from_city,to_city,ttype,duration,price,EURO_ZONE_LOWEST_PRICE))
                    
            price = EURO_ZONE_LOWEST_PRICE
        
    return price


# inner json
def get_inner_json(pth, rt, route_dic):
    try:
        """ if route_dic[pth][8][rt][0] in ['walk', 'car', 'hotel']:
            return 'bad type of transport' """
        if route_dic[pth][8][rt][0] in ['flight', 'fly']:
            return {"path_id": None,
                    "transport":   route_dic[pth][8][rt][0],
                    "air_0":       route_dic[pth][8][rt][2][0],
                    "station_0":   route_dic[pth][8][rt][2][1],
                    "lat_0":       route_dic[pth][8][rt][2][3],
                    "lon_0":       route_dic[pth][8][rt][2][4],
                    "country_0":   route_dic[pth][8][rt][2][6],
                    "city_0":      route_dic[pth][8][rt][2][5],
                    "air_1":       route_dic[pth][8][rt][3][0],
                    "station_1":   route_dic[pth][8][rt][3][1],
                    "lat_1":       route_dic[pth][8][rt][3][3],
                    "lon_1":       route_dic[pth][8][rt][3][4],
                    "country_1":   route_dic[pth][8][rt][3][6],
                    "city_1":      route_dic[pth][8][rt][3][5],
                    "transporter": route_dic[pth][8][rt][2][5],
                    #"dur_path":    route_dic[pth][5],
                    "duration":   route_dic[pth][8][rt][4],
                    "price_min":    route_dic[pth][20][0][0],
                    "price_avg":    route_dic[pth][20][1][0],
                    "price_max":    route_dic[pth][20][2][0],
                    "currency":    route_dic[pth][20][0][1],
                    "frequency":   route_dic[pth][8][rt][8],
                    "num_transfers": len(route_dic[pth][8][rt][12]),
                    "transfers_info": route_dic[pth][8][rt][12]
                    }
        else:
            return {"id": None,
                    "transport":   route_dic[pth][8][rt][1],
                    "station_0":   route_dic[pth][8][rt][6][1],
                    "lat_0":       route_dic[pth][8][rt][6][2],
                    "lon_0":       route_dic[pth][8][rt][6][3],
                    "country_0":   route_dic[pth][8][rt][6][4],
                    "city_0":      route_dic[pth][8][rt][6][5],
                    "station_1":   route_dic[pth][8][rt][7][1],
                    "lat_1":       route_dic[pth][8][rt][7][2],
                    "lon_1":       route_dic[pth][8][rt][7][3],
                    "country_1":   route_dic[pth][8][rt][7][4],
                    "city_1":      route_dic[pth][8][rt][7][5],
                    "transporter": route_dic[pth][8][rt][10][8][0][0],
                    "www":         route_dic[pth][8][rt][10][8][0][2],
                    "phone":       route_dic[pth][8][rt][10][8][0][10],
                    "mail":        route_dic[pth][8][rt][10][8][0][11],
                    "price_min":    route_dic[pth][20][0][0],
                    "price_avg":     route_dic[pth][20][1][0],
                    "price_max":    route_dic[pth][20][2][0],
                    #"cost_t_max":  route_dic[pth][8][rt][13][0][0],
                    #"cost_t_avg":   route_dic[pth][8][rt][13][1][0],
                    #"cost_tr_min": route_dic[pth][8][rt][13][2][0],
                    "currency":    route_dic[pth][20][0][1],
                    "dur_pth_max": route_dic[pth][5]
                    }
    except IndexError as err:
        return "Error:", err 
    
    
def delete_inner_jsons(ids: list[int]):
    deleted, not_exist = 0, 0
    for id in ids:
        id = f'{INNER_JSON_DIR}/{id}.json'
        try:
            os.remove(id)
            print(f"File '{id}' deleted successfully.")
            deleted += 1
        except FileNotFoundError:
            print(f"File '{id}' not found.")
            not_exist += 1
            continue
    print(f'Total processed: {len(ids)} files. Deleted: {deleted} files, not found: {not_exist} files')
    
    
def fixing_price_inner_json(id: int, price: int) -> None:
    with open(f'{INNER_JSON_DIR}/{id}.json', 'r') as file:
        inner_json = json.load(file)
        
    inner_json['prices_EUR']['min'] = price
    
    with open(f'{INNER_JSON_DIR}/{id}.json', 'w') as file:
        json.dump(inner_json, file, indent=4)
        
    
def get_prompts_GPT(prompt_json):
    with open(prompt_json, 'r') as file:
        return json.load(file)
    

def limit_calls_per_minute(max_calls):
    """
    Decorator that limits a function to being called `max_calls` times per minute,
    with a delay between subsequent calls calculated based on the time since the
    previous call.
    """
    calls = []
    def decorator(func):
        def wrapper(prompt, api_key='OPENAI_API_KEY_CT_0'):
            # Remove any calls from the call history that are older than 1 minute
            calls[:] = [call for call in calls if call > time.time() - 60]
            if len(calls) >= max_calls:
                # Too many calls in the last minute, calculate delay before allowing additional calls
                time_since_previous_call = time.time() - calls[-1]
                delay_seconds = 60 / max_calls - time_since_previous_call
                if delay_seconds > 0:
                    time.sleep(delay_seconds)
            # Call the function and add the current time to the call history
            try:
                result = func(prompt, api_key='OPENAI_API_KEY_CT_0')
            except Exception:
                # An exception was raised, trigger a delay and recursive function call with the same parameter
                time.sleep(60)
                return wrapper(prompt, api_key='OPENAI_API_KEY_CT_0')
            calls.append(time.time())
            print('\n',result)
            return result
        return wrapper
    return decorator
    
  
@limit_calls_per_minute(3)    
def get_response_GPT(prompt: str, api_key='OPENAI_API_KEY_CT_0'):
    openai.organization = os.getenv('OPENAI_ID_CT')
    openai.api_key = os.getenv(api_key)
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                                        #{"role": "system", "content": f"Act as an {role}"},
                                                        {"role": "user", "content": prompt}
                                                    ],
                                            temperature=0
                                            )   
    
    return response['choices'][0]['message']['content']
     
    
    
if __name__ == '__main__':
    
    #print(get_id_pair('10-Tel-Aviv-20-Clermont-Ferrand'))
    
    #print(get_id_from_acode('fra'),  get_id_from_acode('hhn'))
    
    #print(get_bb_id([38.4511,68.9642]), type(get_bb_id([38.4511,68.9642]))) """
    
    #input_file_ok(CITIES_COUNTRIES_CSV)
    #print(df_init())
    #print(get_city_name(156))
    
    # ct_link = 'https://cheaptrip.guru/en-US/#/search/myPath?from=Milan&fromID=252&to=Prague&toID=297'
    # params = {"from": "Berlin", "fromID": 123, "to": "Doha", "toID": 252}
    # #print(ct_link)
    # print(get_modify_url(ct_link, params))
    
    print(get_cities())
    pass