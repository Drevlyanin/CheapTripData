import pandas as pd
import json
from time import perf_counter
from pathlib import Path
from contextlib import contextmanager
import requests
from bs4 import BeautifulSoup

from functions import get_city_id, get_modify_url, get_response_GPT, get_prompts_GPT
from config import CITIES_COUNTRIES_CSV, EURO_ZONE, SMM_PROMPTS_JSON, SEO_PROMPTS_JSON, SEO_TEXTS_JSON


def recursive_replace(d, old_str, new_str):
    for k, v in d.items():
        if isinstance(v, dict):
            recursive_replace(v, old_str, new_str)
        if isinstance(v, str):
            d[k] = v.replace(old_str, new_str)
    return d


def get_seo_text(city: str):
    
    # city_id = get_city_id(city)
    # ct_link = 'https://cheaptrip.guru/en-US/#/search/myPath?from=Milan&fromID=252&to=Barcelona&toID=128'
    
    # inserting city name into the prompts
    # prompts = {k: v.replace('[city]', city) for k, v in get_prompts_GPT(SEO_PROMPTS_JSON).items()}
    prompts = recursive_replace(get_prompts_GPT(SEO_PROMPTS_JSON), '[city]', city)
    
    # forms main dict structure
    #city_data = dict()
    
    # getting city description
    # prompt = prompts['description']
    # description = str(get_response_GPT(prompt)).strip('\"').replace('\n\n', '\n')
    prompts['description'] = get_response_GPT(prompts['description']).strip('\"').replace('\n\n', '\n')
    
    
    # getting free attractions list
    # prompt = prompts['attractions']['free']
    # free_attractions = str(get_response_GPT(prompt)).strip('').split(',')
    prompts['lists']['attractions'] = get_response_GPT(prompts['lists']['attractions']).strip(' .').split(', ')
           
    # title processing
    # prompt = prompts['city_title'].replace('[description]', description)
    # title = get_response_GPT(prompt)
    # title = title.strip(' \"')
              
    # work with the content item 'routes':
    # prompt = prompts['city_routes']
    # routes = get_response_GPT(prompt)
    # routes = [route.strip() for route in routes.split('\n')]
    # city_data['routes'] = routes

    # write result in json
    SEO_TEXTS_JSON.mkdir(parents=True, exist_ok=True)  
    with open(f'{SEO_TEXTS_JSON}/{city}.json', 'w') as file:
        json.dump(prompts, file, indent=4)
    
    
def get_seo():
    df_cities_countries = pd.read_csv(CITIES_COUNTRIES_CSV, index_col=0)
    for i, city in enumerate(df_cities_countries['city'].values, start=1):
        print(f'Processing: {i}. {city}', end='...')
        get_seo_text(city)            
        print('successfully!')
    
    
if __name__ == '__main__':
    start = perf_counter()
    get_seo()
    print(perf_counter() - start)
    pass