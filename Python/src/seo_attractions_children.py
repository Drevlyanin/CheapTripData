import json
from pathlib import Path

from functions import get_response_GPT, get_prompts_GPT, get_cities
from config import PROMPTS_DIR, SEO_CITY_ATTRACTIONS_DIR, SEO_CITY_ATTRACTIONS_CHILDREN_DIR


def recursive_replace(d, old_str, new_str):
    for k, v in d.items():
        if isinstance(v, dict):
            recursive_replace(v, old_str, new_str)
        if isinstance(v, str):
            d[k] = v.replace(old_str, new_str)
    return d


def get_attractions_children(city) -> None:
    
    prompts = recursive_replace(get_prompts_GPT(PROMPTS_DIR/'city_attractions_children_pmt.json'), '[city]', city)
    
    data = dict()
    for attraction in attractions:
        prompt_i = prompts['attraction']
        prompt_i = prompt_i.replace('[attraction]', attraction)
        response = get_response_GPT(prompt_i)
        response = response.strip(' ').strip('\"')
        response = response.replace('Title: ', '').replace('\n\n', '\n')
        data[attraction] = dict()
        data[attraction]['text'] = response
        # data[attraction]['summary'] = get_response_GPT(prompts['summary'].replace('[text]', response))
        # data[attraction]['keywords'] = get_response_GPT(prompts['keywords'].replace('[text]', response)).strip(' ').split(', ')
    
    # write result in json
    SEO_CITY_ATTRACTIONS_CHILDREN_DIR.mkdir(parents=True, exist_ok=True)  
    with open(f'{SEO_CITY_ATTRACTIONS_CHILDREN_DIR}/{city}.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    
def get_seo_text():
    # files = Path(SEO_CITY_DESCRIPTIONS_DIR).glob('*.json')
    cities = get_cities()
    for i, city in enumerate(cities, start=1):
        print(f'\nProcessing: {i}. {city}')
        get_seo_text(city) 
        print('...successfully!')
        
    
if __name__ == '__main__':
    get_seo_text()