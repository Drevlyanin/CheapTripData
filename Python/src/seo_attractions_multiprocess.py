import json
from pathlib import Path
import os
from multiprocessing import Pool

from functions import get_response_GPT, get_prompts_GPT
from config import PROMPTS_DIR, SEO_CITY_DESCRIPTIONS_DIR, SEO_CITY_ATTRACTIONS_DIR, ATTRACTIONS_LIST_DIR


def recursive_replace(d, old_str, new_str):
    for k, v in d.items():
        if isinstance(v, dict):
            recursive_replace(v, old_str, new_str)
        if isinstance(v, str):
            d[k] = v.replace(old_str, new_str)
    return d


def get_seo_text(city: str, attractions: list[str], api_key: str) -> None:
    
    prompts = recursive_replace(get_prompts_GPT(PROMPTS_DIR/'city_attractions_pmt.json'), '[city]', city)
    
    data = dict()
    for attraction in attractions:
        response = get_response_GPT(prompts['attraction'].replace('[attraction]', attraction), api_key)
        response = response.strip(' ').strip('\"')
        response = response.replace('Title: ', '').replace('\n\n', '\n')
        data[attraction] = dict()
        data[attraction]['text'] = response
        data[attraction]['summary'] = get_response_GPT(prompts['summary'].replace('[text]', response), api_key)
        data[attraction]['keywords'] = get_response_GPT(prompts['keywords'].replace('[text]', response), api_key).strip(' ').split(', ')
    
    # write result in json
    SEO_CITY_ATTRACTIONS_DIR.mkdir(parents=True, exist_ok=True)  
    with open(f'{SEO_CITY_ATTRACTIONS_DIR}/{city}.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    
def get_seo(files, api_key, process_number):
    for i, file in enumerate(files, start=1):
        city = file.name.partition('.')[0]
        with open(file, 'r') as json_file:
            attractions = json.load(json_file).values()
        print(f'\nProcess: {process_number}, City: {i}.{city}')
        get_seo_text(city, attractions, api_key) 
        print('...successfully!')


def run_processes():
    # Get the list of input files
    input_files = sorted(list(Path(ATTRACTIONS_LIST_DIR).glob('*.json')))
    # Get the list of API keys
    api_keys = ['OPENAI_API_KEY_CT_0', 'OPENAI_API_KEY_CT_1', 'OPENAI_API_KEY_CT_2', 'OPENAI_API_KEY_CT_3']
    # Define the maximum number of processes to use
    max_processes = len(api_keys)
    # Define the batch size
    batch_size = len(input_files) // len(api_keys)
    # Split the input files into batches
    batches = [input_files[i:i+batch_size] for i in range(0, len(input_files), batch_size)]
    # Create a pool of processes to run the script
    pool = Pool(processes=max_processes)
    # Iterate over the API keys and batches
    for i, item in enumerate(zip(batches, api_keys), start=1):
        batch, api_key = item[0], item[1]
    # Run the script using the current API key and batch of input files
        pool.apply_async(get_seo, args=(batch, api_key, i))
    # Close the pool
    pool.close()
    # Wait for all processes to finish
    pool.join()
        
    
if __name__ == '__main__':
    # get_seo()
    run_processes()