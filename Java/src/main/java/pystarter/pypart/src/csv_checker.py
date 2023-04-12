from pathlib import Path
import polars as pl
import csv

from logger import logger_setup


logger = logger_setup()


# checking is it a csv file
def is_csv_file(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            return dialect.delimiter == ',' # assuming delimiter is a comma
    except Exception:
        return False


# checks if the input file exists
def csv_ok(path: Path, check_null: bool = True) -> bool:
    
    try:
        if type(path) == str: path = Path(path)
        
        # checking if the path exists
        if not path.is_file(): raise FileNotFoundError
            
        # checking is it a csv file
        if not is_csv_file(path):
            logger.critical(f"Input file '{path}' is corrupted or not a 'CSV' file !")
            ok = False
            return ok
        
        # trying to read csv    
        with open(path, 'r') as file:
            df = pl.read_csv(file.name)
        
        ok = True # if reading ok
        
        # checking null values in each column
        if check_null:
            for column in df.columns:
                try:    
                    if any(df[column].is_null()): raise ValueError(column)
                except ValueError as err:
                    logger.critical(f"There is a NULL value in column '{err}' in input file: {path} !")
                    ok = False
                    continue    
                
    except FileNotFoundError:
        logger.critical(f"Input file: '{path}' NOT found !")
        ok = False
        
    except Exception as err:
        logger.critical(f"There is a FAILURE while file reading: {err} !")
        ok = False

    finally:
        return ok