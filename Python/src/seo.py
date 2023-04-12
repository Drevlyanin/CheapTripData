import pandas as pd
import json
from time import perf_counter
from pathlib import Path
from pexels import get_pexel_image

from functions import get_city_id, get_modify_url, get_response_GPT, get_prompt_GPT
from config import NOT_FOUND, CITIES_COUNTRIES_CSV, EURO_ZONE


def get_seo_text(city='London'):
    
    #city = 'London'
    city_id = get_city_id(city)
    ct_link = 'https://cheaptrip.guru/en-US/#/search/myPath?from=Milan&fromID=252&to=Barcelona&toID=128'
    prompts = get_prompt_GPT()
    
    with open('../output/cities_info/seo_example.json', 'r') as json_file:
        example_info = json.load(json_file)
    
    with open('../output/cities_info/seo_template.json', 'r') as json_file:
        city_info = json.load(json_file)
    
    for key in filter(lambda x: x != 'content', example_info.keys()):
        city_info[key] = example_info[key].replace('Milan', city)
      
    prompts = [prompt.replace('[city]', city) for prompt in prompts]
      
    # work with the content item 'way'
    city_info['content']['way']['title'] = example_info['content']['way']['title'].replace('Milan', city)
    city_info['content']['way']['description'] = example_info['content']['way']['description'].replace('Milan', city)
            
    # work with the content item 'city'    
    city_info['content']['city']['title'] = example_info['content']['city']['title'].replace('Milan', city)
    city_info['content']['city']['images'] = get_pexel_image(city)   
   
    prompt = prompts[0].replace('[city_description]', example_info['content']['city']['description'])
    
    city_info['content']['city']['description'] = get_response_GPT(prompt)
        
    # work with the content items: 'accomodation', 'eats', 'attractions'
    for key in ['accomodations', 'eats', 'attractions']:
        
        prompt = prompts[1]
        prompt = prompt.replace('[content_key_title]', city_info['content'][key]['title'])
        prompt = prompt.replace('[example_title_description]', example_info['content'][key]['description'])
        city_info['content'][key]['description'] = get_response_GPT(prompt)
        
        prompt = prompts[2]
        prompt = prompt.replace('[count]', str(city_info['content'][key]['count']))
        prompt = prompt.replace('[content_key_title]', city_info['content'][key]['title'])
        names = get_response_GPT(prompt)
        
        for name in names.split('\n'):
            prompt = prompts[3]
            prompt = prompt.replace('[name]', name)
            prompt = prompt.replace('[content_key_title]', city_info['content'][key]['title'])
            prompt = prompt.replace('[example_option_description]', example_info['content'][key]['options'][0]['description'])
            description = get_response_GPT(prompt)
            
            prompt = prompts[4]
            prompt = prompt.replace('[name]', name)
            prompt = prompt.replace('[content_key_title]', city_info['content'][key]['title'])
            prompt = prompt.replace('[example_option_location]', example_info['content'][key]['options'][0]['location'])
            location = get_response_GPT(prompt)
            
            city_info['content'][key]['options'].append({'name':name,'description':description,'location':location})
    
    # work with the content items: 'tours' and 'transportation':
    for key in ['tours', 'transportations']:
        prompt = prompts[5]
        prompt = prompt.replace('[content_key_title]', city_info['content'][key]['title'])
        prompt = prompt.replace('[example_title_description]', example_info['content'][key]['description'])
        description = get_response_GPT(prompt)
        
        prompt = prompts[6]
        prompt = prompt.replace('[content_key_title]', city_info['content'][key]['title'])
        prompt = prompt.replace('[content_key_description]', description)
        links = get_response_GPT(prompt)
        
        city_info['content'][key]['description'] = description
        city_info['content'][key]['links'] = links.split('\n')
        
    # work with the content item 'routes':
    # city_info['content']['routes']['title'] += city
    
    # prompt = prompts[7]
    # prompt = prompt.replace('[content_key_title]', city_info['content']['routes']['title'])
    # city_info['content']['routes']['description'] = get_response_GPT(prompt)
    
    # prompt = prompts[8]
    # prompt = prompt.replace('[count]', str(city_info['content']['routes']['count']))
    # routes = get_response_GPT(prompt)
    
    # for route in routes.split('\n'):
        
    #     route_id = get_city_id(route)
        
    #     if route_id == NOT_FOUND: continue
        
    #     prompt = prompts[9]
    #     prompt = prompt.replace('[route]', route)
    #     prompt = prompt.replace('[example_route_description]', example_info['content']['routes']['pathes'][0]['description'])
    #     description = get_response_GPT(prompt)
        
    #     params = {"from": city, "fromID": city_id, "to": route, "toID": route_id}
    #     ct_link = get_modify_url(ct_link, params)
    
    #     city_info['content']['routes']['pathes'].append({'route':route, 'description':description, 'link':ct_link})
    
    # write result in json  
    with open(f'../output/cities_info/{city}.json', 'w') as file:
        json.dump(city_info, file, indent=4)   
          

def get_seo():
    df_cities_countries = pd.read_csv(CITIES_COUNTRIES_CSV, header=0, index_col=0)
    for i, city in enumerate(df_cities_countries.loc[df_cities_countries.index.isin(EURO_ZONE)]['city'].values, start=1):
        print(f'Processing: {i}. {city}', end='...')
        get_seo_text(city)
        print('successfully!')
        
    #df.loc[df['Age'].isin(range(30, 51))]
    #print(df_cities_countries.loc[df_cities_countries.index.isin(EURO_ZONE)]['city'].values)
    
    
if __name__ == '__main__':
    start = perf_counter()
    get_seo_text()
    print(perf_counter() - start)
    pass