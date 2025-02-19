'''
Module for normalizing either the wsjgainers.csv file or the ygainers.csv file. Produces
new .csv files named: "[original-file]_norm.csv".

Normalized csv files contain the following features:
    symbol
    price
    price_cange
    price_percent_change
'''

import sys
import re
import pandas as pd

def import_wsjgainers(wsj_data):
    '''
    Function for normalizing the wsjgainers.csv file, determined by file name outside this
    function and confirmed by column count at function start. Returns normalized dataframe.
    '''
    assert len(wsj_data.columns) == 6, f"\nExpected 6 columns, found {len(wsj_data.columns)}\n"

    wsj_data = wsj_data[['Unnamed: 0', 'Last', 'Chg', '% Chg']].rename(
            columns={
                'Unnamed: 0':'symbol', 
                'Last':'price', 
                'Chg':'price_change', 
                '% Chg':'price_percent_change'
                })

    wsj_data['symbol'] = wsj_data['symbol'].replace(
            r'.*[(]', '', regex=True).replace(r'[)].*', '', regex=True)

    return wsj_data

def import_ygainers(y_data):
    '''
    Function for normalizing the ygainers.csv file, determined by file name outside this
    function and confirmed by column count at function start. Returns normalized dataframe.
    '''
    assert len(y_data.columns) == 13, f"\nExpected 13 columns, found {len(y_data.columns)}\n"

    y_data = y_data[['Symbol', 'Price', 'Change', 'Change %']].rename(
            columns={
                'Symbol':'symbol', 
                'Price':'price', 
                'Change':'price_change', 
                'Change %':'price_percent_change'
                })

    y_data['price'] = pd.to_numeric(y_data['price'].str.split(' ').str[0])
    y_data['price_percent_change'] = pd.to_numeric(
            y_data['price_percent_change'].replace(r'[^0-9.]', '', regex=True))

    return y_data

data_path = sys.argv[1] # The path passed when calling the script
data_name = re.sub(r'[.]csv$', '', re.sub(r'^.*[/]', '', data_path))

try:
    raw_data = pd.read_csv(data_path)
except FileNotFoundError:
    print('''\nThere was a problem importing the data:
          make sure your file is a csv and check the path for errors.\n''')

if data_name == "wsjgainers":
    normalized_data = import_wsjgainers(raw_data)
else:
    normalized_data = import_ygainers(raw_data)

assert isinstance(normalized_data['symbol'][0], str),\
        f'''Expected "symbol" to contain string type,
        , but instead found type: {type(normalized_data["symbol"][0])}'''

assert isinstance(normalized_data['price'][0], float),\
        f'''Expected "price" to contain float type
        , but instead found type: {type(normalized_data["price"][0])}'''

assert isinstance(normalized_data['price_change'][0], float),\
        f'''Expected "price_change" to contain float type
        , but instead found type: {type(normalized_data["price_change"][0])}'''

assert isinstance(normalized_data['price_percent_change'][0], float), \
        f'''Expected "price_percent_change" to contain float type
        , but instead found type: {type(normalized_data["price_percent_change"][0])}'''

write_path = re.sub('[.]csv$', '_norm.csv', data_path)
normalized_data.to_csv(write_path, index=False)

print(f"\nThe data has been normalized and exported to: {write_path}\n")
