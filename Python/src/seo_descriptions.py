import pandas as pd
import json
from time import perf_counter

from functions import get_response_GPT, get_prompts_GPT
from config import CITIES_COUNTRIES_CSV, SEO_PROMPTS_JSON, SEO_CITY_DESCRIPTIONS_DIR


def recursive_replace(d, old_str, new_str):
    for k, v in d.items():
        if isinstance(v, dict):
            recursive_replace(v, old_str, new_str)
        if isinstance(v, str):
            d[k] = v.replace(old_str, new_str)
    return d


def get_seo_text(city: str):
    
    # replace city in prompt
    prompts = recursive_replace(get_prompts_GPT(SEO_PROMPTS_JSON), '[city]', city)
    
    # getting city description and attractions list
    prompts['description'] = get_response_GPT(prompts['description']).strip('\"').replace('\n\n', '\n')
    prompts['lists']['attractions'] = get_response_GPT(prompts['lists']['attractions']).strip(' .').split(', ')

    # write result in json
    SEO_CITY_DESCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)  
    with open(f'{SEO_CITY_DESCRIPTIONS_DIR}/{city}.json', 'w') as file:
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