import json
from pathlib import Path

from functions import get_response_GPT, get_prompts_GPT
from config import PROMPTS_DIR, SEO_CITY_DESCRIPTIONS_DIR, SEO_CITY_ATTRACTIONS_DIR, OPTION_LISTS_DIR

    
def make_lists():
    files = sorted(list(Path(SEO_CITY_DESCRIPTIONS_DIR).glob('*.json')))
    for i, file in enumerate(files, start=1):
        city = file.name.partition('.')[0]
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            attractions = content['lists']['attractions']
            content.pop('lists')
        with open(file, 'w') as json_file:
            json.dump(content, json_file, indent=4)
        
        data = dict()
        for i, attraction in enumerate(attractions, start=1):
            data[i] = attraction
        
        with open(f'{OPTION_LISTS_DIR}/attractions/{city}.json', 'w') as f:
            json.dump(data, f, indent=4)
        
    
if __name__ == '__main__':
    make_lists()