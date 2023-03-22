import pandas as pd


from config import CITIES_COUNTRIES_CSV, AIRPORT_CODES_CSV, CITIES_CSV, IATA_CODES_CSV, BBOXES_CSV
from functions import get_bboxes
from csv_checker import csv_ok


def get_airport_codes():
    
    try:
        
        df_cities_countries = pd.read_csv(CITIES_COUNTRIES_CSV, header=0, index_col=0)
        df_iata_codes = pd.read_csv(IATA_CODES_CSV, header=0, index_col=0)
        
        if AIRPORT_CODES_CSV.is_file():
            df_airport_codes = pd.read_csv(AIRPORT_CODES_CSV, header=0, dtype={'id_city':'Int32'}, index_col=0)
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
        df_airport_codes.to_csv(AIRPORT_CODES_CSV)
        df_airport_codes = pd.read_csv(AIRPORT_CODES_CSV, header=0, dtype={'id_city':'Int32'}, index_col=0)
        df_airport_codes.to_csv(AIRPORT_CODES_CSV)
        
    except FileNotFoundError as err:
        print(err)          
                
                
def get_bounding_boxes():
    
    try:
        df_cities_countries = pd.read_csv(CITIES_COUNTRIES_CSV, header=0, index_col=0)
        
        if BBOXES_CSV.is_file():
            df_bboxes = pd.read_csv(BBOXES_CSV, header=0, index_col=0)
            unboxed_ids = set(df_cities_countries.index.values).difference(df_bboxes.index.values)
            if len(unboxed_ids) == 0: 
                print('Go on: all bounding boxes are already exist!\n')
                return
        else:
            df_bboxes = pd.DataFrame()
            unboxed_ids = df_cities_countries.index.values
            
        if CITIES_CSV.is_file():
            df_cities = pd.read_csv(CITIES_CSV, header=0, index_col=0)
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
        df_bboxes.to_csv(BBOXES_CSV)
        df_cities.to_csv(CITIES_CSV)
        
        
    except FileNotFoundError as err:
        print(err)
    
    except Exception as err:
        print(err)    


def preextract():
    if csv_ok(IATA_CODES_CSV, check_null=False) and csv_ok(CITIES_COUNTRIES_CSV):
        print('\nPreextraction process started...')
        get_airport_codes()
        get_bounding_boxes()
        print('Preextraction completed successfully!')
        return True
    return False

if __name__ == '__main__':
    preextract()