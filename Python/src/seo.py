import pandas as pd
import openai
import os
import json
from time import perf_counter
from pathlib import Path
from pexels import get_pexel_image


def get_seo_text():
    
    openai.organization = "org-2enZa8BZcwVTWlVOMiFLwb6r"
    openai.api_key = os.getenv('OPENAI_API_KEY_CT')
    
    city = 'Berlin'
    
    with open('../output/cities_info/seo_template_Milan_origin.json', 'r') as json_file:
        city_info = json.load(json_file)
        
    for key, value in filter(lambda item: item[0] != 'content', city_info.items()):
        city_info[key] = value.replace('Milan', city)
        
    # work with the content item 'way'
    city_info['content']['way']['title'] = city_info['content']['way']['title'].replace('Milan', city)
    city_info['content']['way']['description'] = city_info['content']['way']['description'].replace('Milan', city)
            
    # work with the content item 'city'    
    city_info['content']['city']['title'] = city_info['content']['city']['title'].replace('Milan', city)
    city_info['content']['city']['images'] = get_pexel_image(city)
    
    # ask ai to generate a city description        
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                    #{"role": "system", "content": "Act as an advanced seo expert."},
                    {"role": "user", "content": f"""Write a seo-frendly description of the city of {city} 
                        like in this example: {city_info['content']['city']['description']}.
                        Your target audience is budget travellers."""}
                ],
        #temperature=0.0
                                            )   
    city_info['content']['city']['description'] = response['choices'][0]['message']['content']
        
    # work with the content items: 'accomodation', 'eats', 'attractions'
    for key in ['accomodation', 'eats', 'attractions']:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                        #{"role": "system", "content": f"Act as an expert level {city} guide with 10+ years of experience."},
                        {"role": "user", "content": f"""Write a short description of {city_info['content'][key]['title']} 
                                                        options in the city of {city} for budget travellers, like in this example: 
                                                        {city_info['content'][key]['description']}"""
                        }
                    ],
            #temperature=0.0
                                                )
        city_info['content'][key]['description'] = response['choices'][0]['message']['content']
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                        #{"role": "system", "content": f"Act as an expert level {city} guide with 10+ years of experience."},
                        {"role": "user", "content": f"""Find {city_info['content'][key]['title']} options 
                                                        in the city of {city} with descriptions and location links, 
                                                        like in this example: {city_info['content'][key]['items'][0]}. 
                                                    """
                        }
                    ],
            #temperature=0.0
                                                )
        city_info['content'][key]['items'] = response['choices'][0]['message']['content']
    
    # work with the content items: 'tours' and 'transportation':
    for key in ['tours', 'transportation']:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                        #{"role": "system", "content": f"Act as an expert level {city} guide with 10+ years of experience."},
                        {"role": "user", "content": f"""Write a short description of {city_info['content'][key]['title']} 
                                                        options in the city of {city} for budget travellers, like in this example: 
                                                        {city_info['content'][key]['description']}"""
                        }
                    ],
            #temperature=0.0
                                                )
        city_info['content'][key]['description'] = response['choices'][0]['message']['content']
    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                        #{"role": "system", "content": f"Act as an expert level {city} guide with 10+ years of experience."},
                        {"role": "user", "content": f"""Provide a list of relevant links for this description 
                                                    {city_info['content'][key]['description']} of the
                                                    {city_info['content'][key]['title']} options in the city of {city}"""
                        }
                    ],
            #temperature=0.0
                                                )
        city_info['content'][key]['link'] = response['choices'][0]['message']['content']
        
    # work with the content item 'routes':
    city_info['content']['routes']['title'] = city_info['content']['routes']['title'].replace('Milan', city)
    city_info['content']['routes']['description'] = city_info['content']['routes']['description'].replace('Milan', city)
    
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                        #{"role": "system", "content": f"Act as an expert level {city} guide with 10+ years of experience."},
                        {"role": "user", "content": f"""Provide me with a list of 10 most popular routes from {city} 
                                                        to other attractive cities in Europe with short seo-frendly route descriptions
                                                        relevant to budget travellers, like in this example: 
                                                        ['route':'{city} to Lisbon', 
                                                        'description': {city_info['content']['routes']['items'][3]['description']}]."""
                        }
                    ],
            #temperature=0.0
                                            )
    routes = response['choices'][0]['message']['content']
    
    city_info['content']['routes']['items'] = routes
      
    with open(f'../output/cities_info/{city}.json', 'w') as file:
        json.dump(city_info, file, indent=4)   
          
    
    #print(response['choices'][0]['finish_reason'])
    """ response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        temperature=0,
                                        max_tokens=2500) """
              
    """ response_img = openai.Image.create(
                                        #prompt=response['choices'][0]['message']['content'],
                                        prompt="Brandenburg Gate in black and white colors",
                                        n=5,
                                        size="1024x1024"
                                        
                                        ) """
    
    #print(response['choices'][0]['text'])
      
    
    
if __name__ == '__main__':
    start = perf_counter()
    get_seo_text()
    print(perf_counter() - start)
    pass