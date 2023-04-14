import pandas as pd
import json
from time import perf_counter
from pathlib import Path
from pexels import get_pexel_image
from contextlib import contextmanager

from functions import get_city_id, get_modify_url, get_response_GPT, get_prompts_GPT
from config import NOT_FOUND, CITIES_COUNTRIES_CSV, EURO_ZONE


@contextmanager
def nested_dict(dicts: tuple(), keys: tuple) -> dict:
    nd, nd2 = dicts
    for key in keys:
        nd = nd.setdefault(key, {})
        nd2 = nd2.setdefault(key, {})
    yield nd, nd2


def get_seo_text(*, city='Kuressaare'):
    
    city_id = get_city_id(city)
    ct_link = 'https://cheaptrip.guru/en-US/#/search/myPath?from=Milan&fromID=252&to=Barcelona&toID=128'
    
    prompts = {k: v.replace('[city]', city) for k, v in get_prompts_GPT().items()}
    
    with open('../output/cities_info/seo_example.json', 'r') as json_file:
        example_info = json.load(json_file)
    
    # forms main dict structure
    city_info = dict.fromkeys(('description', 'keywords', 'title', 'content'))
    city_info['content'] = {key: {} for key in ('way', 'city', 'accomodations', 'eats', 
                                                'attractions', 'tours', 'transportations', 'routes')}
    
    # work with 'description', 'keywords', 'title'
    for key in filter(lambda x: x != 'content', city_info.keys()):
        city_info[key] = example_info[key].replace('Milan', city)
    
    # work with the 'content' 'way' item 
    with nested_dict((city_info, example_info), ('content', 'way')) as (c, e):
        for key in ('title', 'description'):
            c[key] = e[key].replace('Milan', city)
        c['link'] ="https://cheaptrip.guru/en-US/#/search/myPath/logo"
       
    # work with the 'content' 'city' item 
    with nested_dict((city_info, example_info), ('content', 'city')) as (c, e):
        c['title'] = e['title'].replace('Milan', city)
        prompt = prompts['city_descr'].replace('[description]', e['description'])
        c['description'] = get_response_GPT(prompt)
        c['images'] = get_pexel_image(city)   
        
    # work with the content items: 'accomodation', 'eats', 'attractions'
    for key in ('accomodations', 'eats', 'attractions'):
        with nested_dict((city_info, example_info), ('content', key)) as (c, e):
            prompt = prompts['aea_descr'].replace('[title]', e['title'])
            prompt = prompt.replace('[description]', e['description'])
            c['description'] = get_response_GPT(prompt)
        
            prompt = prompts['aea_opts'].replace('[title]', e['title'])
            names = get_response_GPT(prompt)

            names = names.split('\n')
            if len(names) == 1: names = names[0].split(',')
            names = [name.strip(' .') for name in names]
            
            c['options'] = []
            for name in names:
                prompt = prompts['aea_opt_descr'].replace('[name]', name)
                prompt = prompt.replace('[title]', e['title'])
                prompt = prompt.replace('[description]', e['options'][0]['description'])
                description = get_response_GPT(prompt)
                
                prompt = prompts['aea_opt_loc'].replace('[name]', name)
                prompt = prompt.replace('[title]', e['title'])
                prompt = prompt.replace('[location]', e['options'][0]['location'])
                location = get_response_GPT(prompt)
                
                c['options'].append({'name':name,'description':description,'location':location})
    
    # work with the content items: 'tours' and 'transportation':
    for key in ('tours', 'transportations'):
        with nested_dict((city_info, example_info), ('content', key)) as (c, e):
            prompt = prompts['tt_descr'].replace('[title]', e['title'])
            prompt = prompt.replace('[description]', e['description'])
            description = get_response_GPT(prompt)
            
            prompt = prompts['tt_links'].replace('[title]', e['title'])
            prompt = prompt.replace('[description]', description)
            links = get_response_GPT(prompt)
            
            c['description'] = description
            c['links'] = [link.strip('- ') for link in links.split('\n')]
        
    # work with the content item 'routes':
    with nested_dict((city_info, example_info), ('content', 'routes')) as (c, e):
        c['title'] = e['title'].replace('Milan', city)
        
        prompt = prompts['ro_descr'].replace('[title]', c['title'])
        c['description'] = get_response_GPT(prompt)
        
        routes = get_response_GPT(prompts['ro_ro'])
        routes = routes.split('\n')
        if len(routes) == 1: routes = routes[0].split(',')
        routes = [route.strip(' .') for route in routes]
        
        c['pathes'] = []
        for route in routes:
            
            route_id = get_city_id(route)
            
            if route_id == NOT_FOUND: continue
            
            prompt = prompts['ro_ro_descr'].replace('[route]', route)
            prompt = prompt.replace('[description]', e['pathes'][1]['description'])
            description = get_response_GPT(prompt)
            
            params = {"from": city, "fromID": city_id, "to": route, "toID": route_id}
            ct_link = get_modify_url(ct_link, params)
        
            c['pathes'].append({'route':route, 'description':description, 'link':ct_link})
    
    # write result in json  
    with open(f'../output/cities_info/{city}.json', 'w') as file:
        json.dump(city_info, file, indent=4)   
          

def get_seo():
    df_cities_countries = pd.read_csv(CITIES_COUNTRIES_CSV, header=0, index_col=0)
    for i, city in enumerate(df_cities_countries.loc[df_cities_countries.index.isin(EURO_ZONE)]['city'].values, start=1):
        print(f'Processing: {i}. {city}', end='...')
        get_seo_text(city)
        print('successfully!')

    
if __name__ == '__main__':
    start = perf_counter()
    get_seo_text()
    print(perf_counter() - start)
    pass