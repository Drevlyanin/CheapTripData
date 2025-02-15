from pathlib import Path


BASE_URL = 'https://www.rome2rio.com/map/'
NOT_FOUND = -1
BAD_VALUES = (0, '', ' ')

# logs set up
LOGS_DIR = Path('../logs')

# set up inputs
INPUT_CSV_DIR = Path('../files/csv')
AIRPORT_CODES_CSV = Path(INPUT_CSV_DIR/'airport_codes.csv')
IATA_CODES_CSV = Path('../files/airports/iata_codes.csv')
BBOXES_CSV = Path(INPUT_CSV_DIR/'bounding_boxes.csv')
CITIES_COUNTRIES_CSV = Path(INPUT_CSV_DIR/'cities_countries.csv')
CITIES_CSV = Path(INPUT_CSV_DIR/'cities.csv')

# set up outputs folders
OUTPUT_JSON_DIR = Path('../output_5run/jsons')
OUTPUT_CSV_DIR = Path('../output/csv')
INNER_JSON_DIR = Path('../output/routes_info')
HOTELS_DIR = Path('../files/hotels')
ROUTES_TO_FIX_DIR = Path('../files/routes_to_fix')

# set up csvs file names
RAW_CSV = Path(OUTPUT_CSV_DIR/'all_direct_routes_raw.csv')
VALIDATION_CSV = Path(OUTPUT_CSV_DIR/'all_direct_routes_validation.csv')
TRIPLES_CSV = Path(OUTPUT_CSV_DIR/'all_direct_routes_triples.csv')
ROUTES_TO_FIX_CSV = Path(ROUTES_TO_FIX_DIR/'routes_to_fix.csv')
FIXED_IDS_CSV = Path(OUTPUT_CSV_DIR/'fixed_ids.csv')
VALID_ROUTES_CSV = Path(OUTPUT_CSV_DIR/'all_direct_valid_routes.csv')
MISSING_PAIRS = Path(OUTPUT_CSV_DIR/'missed_pairs.csv')

#set up currencies
CURRENCY_EXCHANGE_RATES_DIR = Path('../files/currencies')
CURRENCY_JSON = Path(CURRENCY_EXCHANGE_RATES_DIR/'exchange_rates_EUR.json')
CURRENCY_HRK = Path(CURRENCY_EXCHANGE_RATES_DIR/'last_HRK_EUR_rates.json')

# excluded cities as unimportant
EXCLUDED_CITIES = ('19', '47', '185', '221', '361', 
                   '49', '110', '143', '144', '182', 
                   '188', '223', '238', '298', '313', 
                   '322', '328', '344', '355')

# set up output columns
OUTPUT_COLUMNS = ('path_id', 'origin_id', 'destination_id', 'inner_path_id', 'route_id', 'from_id', 'to_id', 
                  'transport_id', 'price_min_EUR', 'duration_min', 'distance_km', 'frequency_tpw', 'num_transfers') #, 'transfers')

# these items can be extracted from the scrapped json
AVALIABLE_DATA = ('from_city_id', 'from_city', 'to_city_id', 'to_city', 'path_id', 'path_name', 
                  'from_node', 'to_node', 'from_id', 'to_id', 'transport', 'transport_id', 
                  'from_airport', 'to_airport', 'price_min_EUR', 'price_max_EUR', 'price_local', 
                  'currency_local', 'distance_km', 'duration_min')

# cities with specific symbol in the name
DASH_NAME_CITIES = ('Tel-Aviv', 'Cluj-Napoca', 'Clermont-Ferrand', 'Chambery-Savoie', 'Ivano-Frankivsk', 'Winston-Salem',
                    'Yuzhno-Sakhalinsk', 'Petropavlovsk-Kamchatsky', 'Khanty-Mansiysk', 'Gorno-Altaysk', 'Ust-Kut', 
                    'Nikolaevsk-na-Amure', 'Ust-Maya', 'Ust-Nera', 'Ust-Kuyga', 'Naryan-Mar')

# for Trans Nicolaescu case
ROMANIAN_CITIES = (338, 357, 134, 153, 268)
TRANS_NICOLAESCU = 'Trans Nicolaescu'

# set transport types and ids
TRANSPORT_TYPES = {'fly': ('fly', 'flight', 'plane'), 
                    'bus': ('bus', 'busferry', 'nightbus'), 
                    'train': ('train', 'nighttrain'),
                    'share': 'rideshare', 
                    'ferry': ('ferry', 'carferry', 'trainferry')}
TRANSPORT_TYPES_ID = {'fly': 1, 'bus': 2, 'train': 3, 'share': 8, 'ferry': 10}

# set minimal terms for euro zone
EURO_ZONE = range(100, 371)
EURO_ZONE_LOWEST_PRICE, EURO_ZONE_DURATION_LIMIT = 5, 60

# logging set up 
LOGS_DIR = Path('../logs')
LOG_CRITICAL = Path(LOGS_DIR/'critical_errors.log')
LOG_CRITICAL_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# prompts set up
SMM_PROMPTS_JSON = Path('../cities_data/smm/prompts.json')
SEO_PROMPTS_JSON = Path('../cities_data/seo/prompts/city_description_pmt.json')
PROMPTS_DIR = Path('../cities_data/seo/prompts')
SEO_TEXTS_DIR = Path('../cities_data/seo/texts')
SEO_CITY_DESCRIPTIONS_DIR = Path('../cities_data/seo/texts/city_descriptions/en_old')
SEO_CITY_ATTRACTIONS_DIR = Path('../cities_data/seo/texts/city_attractions/en')
SEO_CITY_ATTRACTIONS_CHILDREN_DIR = Path('../cities_data/seo/texts/city_attractions_children/en')
SEO_CITY_ATTRACTIONS_FP_DIR = Path('../cities_data/seo/texts/city_attractions_first_person/en')
SEO_HTMLS_DIR = Path('../cities_data/seo/htmls')
OPTION_LISTS_DIR = Path('../cities_data/option_lists')
ATTRACTIONS_LIST_DIR = Path(OPTION_LISTS_DIR/'attractions')

# directory for images from pexel
PEXEL_IMG_DIR = Path('../output/cities_info/images')