import pandas as pd
import logging
from pathlib import Path

from functions import delete_inner_jsons, fixing_price_inner_json
from config import TRIPLES_CSV, FIXED_IDS_CSV, VALID_ROUTES_CSV, LOGS_DIR, ROUTES_TO_FIX_DIR


logging.basicConfig(filename=LOGS_DIR/'fixing.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def fixing_price():
    files = Path(ROUTES_TO_FIX_DIR).glob('*.csv')
    for file in files:
        fix_price(file)


def fix_price(input_csv):
    
    input_csv = Path(input_csv)
    
       
    if not input_csv.is_file():
        raise FileNotFoundError(input_csv)
        
    print(f"Price fixing from '{input_csv}'...")
        
    df_input = pd.read_csv(input_csv, usecols=['from_id', 'to_id', 'transport_id', 'price_to_fix'], 
                               dtype={'from_id': 'Int32', 'to_id': 'Int32', 'transport_id': 'Int32', 'price_to_fix': 'Int32'})
              
    if not FIXED_IDS_CSV.is_file():
        with open(FIXED_IDS_CSV, 'w') as val_file:
                val_file.write('path_id')
    df_fixed_ids = pd.read_csv(FIXED_IDS_CSV, dtype={'path_id': 'Int32'})
        
    if not VALID_ROUTES_CSV.is_file():
        df_triples = pd.read_csv(TRIPLES_CSV, index_col=0, dtype={'from_id': 'Int32', 'to_id': 'Int32', 'transport_id': 'Int32', 
                                                                      'price_min_EUR': 'Int32', 'duration_min': 'Int32', 'num_transfers':'Int32'})
        df_triples.to_csv(VALID_ROUTES_CSV)
        
    df_output = pd.read_csv(VALID_ROUTES_CSV, index_col=0, dtype={'from_id': 'Int32', 'to_id': 'Int32', 'transport_id': 'Int32', 
                                                                      'price_min_EUR': 'Int32', 'duration_min': 'Int32', 'num_transfers':'Int32'})
           
    query_1 = 'from_id == @from_id and to_id == @to_id and transport_id == @transport_id'
    query_2 = 'from_id == @to_id and to_id == @from_id and transport_id == @transport_id'
        
    fixed = 0
    for query in (query_1, query_2):
        for from_id, to_id, transport_id, price_to_fix in df_input.values:
                
            # executes query
            index = df_output.query(query).index
            print(index)
                    
            # if no matches found    
            if index.empty: 
                print(f'{from_id} {to_id} {transport_id} {price_to_fix} empty')
                continue
                    
            # if match is already in fixed list     
            if index.values[0] in df_fixed_ids['path_id'].values: 
                print(f'{index.values[0]} in path_id')
                continue
                            
            # fixes price in csv as well as in inner_json and adds index to fixed ids
            if price_to_fix == 0:
                print('price_to_fix == 0')
                df_output.drop(index, inplace=True)
                df_fixed_ids.at[df_fixed_ids.shape[0], 'path_id'] = index.values[0]
                delete_inner_jsons(index)
                continue
                    
            print('before price changing')    
            df_output.at[index, 'price_min_EUR'] = price_to_fix
            fixing_price_inner_json(index.values[0], price_to_fix)
            df_fixed_ids.at[df_fixed_ids.shape[0], 'path_id'] = index.values[0]
            fixed += 1

            
    df_output.sort_index(inplace=True) 
    df_output.to_csv(VALID_ROUTES_CSV)
        
    df_fixed_ids.sort_values(by='path_id', inplace=True)
    df_fixed_ids.to_csv(FIXED_IDS_CSV, index=None)
                
    print(f'Totally processed: {df_input.shape[0] * 2} routes. Fixed successfully: {fixed} routes.')
                

if __name__ == '__main__':
    
    fixing_price()
    # if len(sys.argv) >= 1 or sys.argv[1] == '-b':
    #     files = Path(ROUTES_TO_FIX_DIR).glob('*.csv')
    #     for file in files:
    #         fix_price(file)
            
    # elif len(sys.argv) > 2 and sys.argv[1] == '-f':
    #     fix_price(Path(ROUTES_TO_FIX_DIR)/sys.argv[2])