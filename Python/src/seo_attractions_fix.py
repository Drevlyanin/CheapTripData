import json
from pathlib import Path
import re

from config import SEO_CITY_ATTRACTIONS_DIR, SEO_CITY_ATTRACTIONS_FP_DIR
        
        
def fixing_routine(data: dict, city: str):
    # - to .
    data = {k: v.replace('-Guru', '.Guru') for k, v in data.items()}
    
    for key, value in data.items():
        
        value = value.split('\n')
        if value[0][-1] != '!':
            value[0] += '!'
        value = '\n'.join(value)
        
        data[key] = dict()
        data[key]['text'] = value
        data[key]['hashtags'] = re.findall(r"#\w+", value)
        data[key]['text'] = re.sub(r"#(\w+)", "", data[key]['text'])
        data[key]['text'] = data[key]['text'].strip(' ')
        data[key]['text'] = data[key]['text'].replace('hashtags  and  ', 'hashtags ')
        data[key]['text'] = data[key]['text'].replace('hashtags  and .', 'hashtags.')
        data[key]['text'] = data[key]['text'].replace('hashtags     to', 'hashtags to')
        data[key]['text'] = data[key]['text'].replace('with  and  ', '')
        data[key]['text'] = data[key]['text'].replace('with   .', '')
        data[key]['text'] = data[key]['text'].replace('.Until', '. Until')  
        data[key]['text'] = data[key]['text'].replace(',CheapTrip.Guru', ', CheapTrip.Guru')
        data[key]['text'] = data[key]['text'].replace('     gem', '')
        data[key]['text'] = data[key]['text'].replace('  and !Happy', '! Happy')
        data[key]['text'] = data[key]['text'].replace('Hashtags:', '')
        data[key]['text'] = data[key]['text'].replace('with    to share', 'to share')
        data[key]['text'] = data[key]['text'].replace('hashtags   .', 'hashtags.')
        data[key]['text'] = data[key]['text'].replace("   'sSquare", '')
        data[key]['text'] = data[key]['text'].replace('hashtags    to share', 'hashtags to share')
        data[key]['text'] = data[key]['text'].replace(' .', '.')
        
    # write result in json
    SEO_CITY_ATTRACTIONS_DIR.mkdir(parents=True, exist_ok=True)  
    with open(f'{SEO_CITY_ATTRACTIONS_DIR}/{city}.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    
def fix_seo():
    files = sorted(list(Path(SEO_CITY_ATTRACTIONS_FP_DIR).glob('*.json')))
    for i, file in enumerate(files, start=1):
        city = file.name.partition('.')[0]
        with open(file, 'r') as json_file:
            data = json.load(json_file)
        print(f'\nProcessing: {i}. {city}')
        fixing_routine(data, city) 
        print('...successfully!')
        
    
if __name__ == '__main__':
    fix_seo()