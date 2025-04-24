'''
Module for reformatting normalized gainer files for output to Snowflake. Produces file
names formatted: "[source]_[YYYYMMDD]_[HHMM].csv"

CSV files still contain the following features:
    symbol
    price
    price_cange
    price_percent_change
'''
import os
import sys
import re
import pandas as pd

def reformat_gainers_files(directory_path):
    '''
    Function that reformats all files in a directory to the format specified above. Filenames
    are expected to originally be in the format: "[source]_gainers_[YYYY-MM-DD]-[HH:MM].csv"
    '''
    csv_list = None
    
    try:
        csv_list = [ff for ff in os.listdir(directory_path) if ff.endswith('.csv')]
    except FileNotFoundError:
        print(f'{directory_path} is not a recognized directory')

    assert csv_list is not None, f'Unable to parse the files in {directory_path}'
    assert len(csv_list) > 0, f'No CSV files were found in {directory_path}'

    pattern = r'^[a-zA-Z]*_gainers_[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}:[0-9]{2}.csv'

    for file in csv_list:
        if re.fullmatch(pattern, file) is not None:
            new_file = re.sub(r'(?P<dash>-)(?=[0-9]{2}:[0-9]{2}.csv$)', r'\g<dash>_', file)
            new_file = new_file.replace("-", "").replace(":", "").replace("_gainers_", "_")
            os.rename(f'{directory_path}/{file}', f'{directory_path}/{new_file}')

if __name__ == "__main__":
    reformat_gainers_files(sys.argv[1])
