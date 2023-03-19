import pandas as pd


from config import CITIES_COUNTRIES_CSV, AIRPORT_CODES_CSV, CITIES_CSV, IATA_CODES_CSV, BBOXES_CSV
from functions import logger_setup, get_bboxes, input_file_ok


df_cities_countries = pd.read_csv(CITIES_COUNTRIES_CSV, names=['id_city', 'city', 'country'], index_col='id_city')
  

def get_airport_codes():
    logger = logger_setup()
    try:
        if not IATA_CODES_CSV.is_file(): raise FileNotFoundError
        
        df_iata_codes = pd.read_csv(IATA_CODES_CSV, names=['code', 'name', 'city', 'country_code', 'country', 'lat', 'lon'], 
                                           index_col='code')
        
        if AIRPORT_CODES_CSV.is_file():
            df_airport_codes = pd.read_csv(AIRPORT_CODES_CSV, names=['code', 'id_city'], index_col='code', dtype={'id_city':'Int32'})
            diff_ids = df_cities_countries.index.difference(df_airport_codes['id_city'].unique())
        else:
            df_airport_codes = pd.DataFrame()
            diff_ids = df_cities_countries.index.values
        
        cities = df_cities_countries.loc[diff_ids]['city'].values
        print(f'\nTrying to get aiport codes for cities: {cities}')  
        
        no_airports_cities = list()        
        for id_city in diff_ids:
            
            city, country = df_cities_countries.loc[id_city, ['city', 'country']]
        
            print(f'\n{city}', end='...')
            
            match_codes = df_iata_codes[df_iata_codes['city'].str.contains(city) & 
                                        df_iata_codes['country'].str.contains(country)].index.values
            
            if len(match_codes) == 0:
                print(f'...has no airports!')
                no_airports_cities.append(city)
                continue
            
            for code in match_codes:
                df_airport_codes.at[code.lower(), 'id_city'] = id_city
                
            print(f'...{match_codes} was added successfully!')
        
        print(f'\nAirports report: processed {len(diff_ids)} cities, '
              f'have no airport(s) {len(no_airports_cities)}: {no_airports_cities}\n')    
        
        df_airport_codes.sort_values(by='id_city', inplace=True)
        df_airport_codes.to_csv(AIRPORT_CODES_CSV, header=False)
        df_airport_codes = pd.read_csv(AIRPORT_CODES_CSV, names=['code', 'id_city'], index_col='code', dtype={'id_city':'Int32'})
        df_airport_codes.to_csv(AIRPORT_CODES_CSV, header=False)
        
    except FileNotFoundError as err:
        logger.critical('FileNotFoundError')
        print(err)          
                
                
def get_bounding_boxes():
    
    try:
        if not CITIES_COUNTRIES_CSV.is_file(): raise FileNotFoundError
        
        if BBOXES_CSV.is_file():
            df_bboxes = pd.read_csv(BBOXES_CSV, names=['id_city', 'lat_min', 'lat_max', 'lon_min', 'lon_max'], index_col='id_city')
            unboxed_ids = set(df_cities_countries.index.values).difference(df_bboxes.index.values)
            if len(unboxed_ids) == 0: 
                print('\nGo on: all bounding boxes are already exist!\n')
                return
        else:
            df_bboxes = pd.DataFrame()
            unboxed_ids = df_cities_countries.index.values
            
        if CITIES_CSV.is_file():
            df_cities = pd.read_csv(CITIES_CSV, names=['id_city', 'city', 'lat', 'lon'], index_col='id_city')
        else:
            df_cities = pd.DataFrame()
        
        for id in unboxed_ids:
            try:
                city_country = df_cities_countries.loc[id, ['city', 'country']].values
                print(f'Adding the bounding box and coordinates for: {id} {city_country}', end='...')
                bbox, coords = get_bboxes(city_country)
                df_bboxes.loc[id, ['lat_min', 'lat_max', 'lon_min', 'lon_max']] = bbox
                df_cities.at[id, 'city'] = city_country[0]
                df_cities.loc[id, ['lat', 'lon']] = coords
                print(f'...successfully!')

            except TypeError as err:
                print(f'Failure!')
                continue
            
            except Exception as err:
                print(err)
                continue
                
        df_bboxes.sort_index(inplace=True)
        df_cities.sort_index(inplace=True)
        df_bboxes.to_csv(BBOXES_CSV, header=False)
        df_cities.to_csv(CITIES_CSV, header=False)
        
        
    except FileNotFoundError as err:
        print(err)
    
    except Exception as err:
        print(err)    


def preextract():
    if input_file_ok([IATA_CODES_CSV, CITIES_COUNTRIES_CSV]):
        get_airport_codes()
        get_bounding_boxes()


if __name__ == '__main__':
    preextract()