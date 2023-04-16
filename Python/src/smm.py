import pandas as pd
import json
from time import perf_counter
from pathlib import Path
from contextlib import contextmanager
import requests
from bs4 import BeautifulSoup

from functions import get_city_id, get_modify_url, get_response_GPT, get_prompts_GPT
from config import NOT_FOUND, CITIES_COUNTRIES_CSV, EURO_ZONE


@contextmanager
def nested_dict(nested_dict: dict, keys: tuple) -> dict:
    for key in keys:
        nested_dict = nested_dict.setdefault(key, {})
    yield nested_dict


def get_seo_text(city='Edinburgh'):
    
    city_id = get_city_id(city)
    ct_link = 'https://cheaptrip.guru/en-US/#/search/myPath?from=Milan&fromID=252&to=Barcelona&toID=128'
    
    # inserting city name into the prompts
    prompts = {k: v.replace('[city]', city) for k, v in get_prompts_GPT().items()}
    
    # load examples
    with open('../output/cities_info/seo/seo_example.json', 'r') as json_file:
        example = json.load(json_file)
    
    # forms main dict structure
    city_data = dict.fromkeys(('title', 'description', 'routes'))
    
    # working with the 'description' and 'title' keys 
    with nested_dict(example, ('content', 'city')) as e:
        prompt = prompts['city_descr']
        description = get_response_GPT(prompt)
        description = description.replace('\n\n', ' ')
        description = description.strip(' \"')
        
        # title processing
        prompt = prompts['city_title'].replace('[description]', description)
        title = get_response_GPT(prompt)
        title = title.strip(' \"')
        
        city_data['title'] = title
        city_data['description'] = description
        
    # work with the content item 'routes':
    prompt = prompts['city_routes']
    routes = get_response_GPT(prompt)
    routes = [route.strip() for route in routes.split('\n')]
    city_data['routes'] = routes
    
    # for route in routes:  
    #     route_id = get_city_id(route)
    #     if route_id == NOT_FOUND: continue
    #     params = {"from": city, "fromID": city_id, "to": route, "toID": route_id}
    #     ct_link = get_modify_url(ct_link, params)
    #     r = requests.get(ct_link) # get responce
    #     soup = BeautifulSoup(r.text, 'html.parser')
    #     print(soup)
        
    # write result in json  
    with open(f'../output/cities_info/smm/{city}.json', 'w') as file:
        json.dump(city_data, file, indent=4)   
          

def get_seo():
    df_cities_countries = pd.read_csv(CITIES_COUNTRIES_CSV, index_col=0)
    for i, city in enumerate(df_cities_countries.loc[df_cities_countries.index.isin(EURO_ZONE)]['city'].values, start=1):
        print(f'Processing: {i}. {city}', end='...')
        get_seo_text(city)
        print('successfully!')

    
if __name__ == '__main__':
    start = perf_counter()
    get_seo()
    print(perf_counter() - start)
    pass