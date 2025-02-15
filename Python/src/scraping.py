import concurrent.futures
import logging
import requests
from bs4 import BeautifulSoup
import json

import compress_json

from config import OUTPUT_JSON_DIR, LOGS_DIR, BASE_URL, OUTPUT_CSV_DIR, CITIES_COUNTRIES_CSV, MISSING_PAIRS
from generators import gen_city_country_pairs, gen_injection
from csv_checker import csv_ok


logging.basicConfig(filename=LOGS_DIR/'scraping.log', filemode='w', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

session = requests.Session()
inject = gen_injection() # injection generator


# writes missed cities pairs
def missed_pairs(missed_pairs):
    
    from_city_id, to_city_id, from_city, from_country, to_city, to_country = missed_pairs
    
    with open(MISSING_PAIRS, mode='a') as f:    
        f.writelines(f'{from_city_id},{to_city_id},{from_city},{from_country},{to_city},{to_country}\n')
        

# scrapping for each city_country pair
def scrap_routine(cities_countries_pairs, injection=''):
    
    from_city_id, to_city_id, from_city, from_country, to_city, to_country = cities_countries_pairs
        
    way = f'{from_city}-{from_country}/{to_city}-{to_country}' + injection # in order to avoid missing pairs  
    
    tmp_url = BASE_URL + way
    
    print('Scraping path: ', way)
    
    # extract all avaliable pathes for each pair
    try:      
        
        r = session.get(tmp_url) # get response
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        pathes_info = soup.find('meta', id="deeplinkTrip") # this tag contists info about all pathes
              
        parsed = json.loads(pathes_info["content"])[2][1]
        
        print(f'Recording path in {from_city_id}-{to_city_id}-{from_city}-{to_city}.json.gz')
        
        target_file = f'{OUTPUT_JSON_DIR}/{from_city_id}-{to_city_id}-{from_city}-{to_city}.json.gz'
        compress_json.dump(parsed, target_file)
        
    except TypeError:
        logging.error(f'On {tmp_url} exception occurred: ', exc_info=True)
        scrap_routine(cities_countries_pairs, injection=next(inject))
    
    except Exception:
        missed_pairs(cities_countries_pairs)
        logging.error(f'An exception occurred: ', exc_info=True)

    
def scrap():
    
    if csv_ok(CITIES_COUNTRIES_CSV):
    
        print('Scraping process started...')
        
        OUTPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_CSV_DIR.mkdir(parents=True, exist_ok=True)
        
        # threads running 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(scrap_routine, gen_city_country_pairs())
            
        print('\nScraping completed successfully!') 
         
         
if __name__ == '__main__':
   
    scrap()
  
