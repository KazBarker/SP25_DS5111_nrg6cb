import sys
import pandas as pd
import re

def import_wjsgainers(wjs_data):
	assert len(wjs_data.columns) == 6, f"\nExpected 6 columns, found {len(wjs_data.columns)}\n"

	wjs_data = wjs_data[['Unnamed: 0', 'Last', 'Chg', '% Chg']].rename(columns={'Unnamed: 0':'symbol', 'Last':'price', 'Chg':'price_change', '% Chg':'price_percent_change'})
	wjs_data['symbol'] = wjs_data['symbol'].replace(r'.*[(]', '', regex=True).replace(r'[)].*', '', regex=True)

	return wjs_data

def import_ygainers(y_data):
	assert len(y_data.columns) == 13, f"\nExpected 13 columns, found {len(y_data.columns)}\n"

	y_data = y_data[['Symbol', 'Price', 'Change', 'Change %']].rename(columns={'Symbol':'symbol', 'Price':'price', 'Change':'price_change', 'Change %':'price_percent_change'})
	y_data['price'] = pd.to_numeric(y_data['price'].str.split(' ').str[0])
	y_data['price_percent_change'] = pd.to_numeric(y_data['price_percent_change'].replace(r'[^0-9.]', '', regex=True))

	return y_data


data_path = sys.argv[1]
data_name = re.sub(r'[.]csv$', '', re.sub(r'^.*[/]', '', data_path))

try: raw_data = pd.read_csv(data_path)
except: print("\nThere was a problem importing the data: make sure your file is a csv and check the path for errors.\n")

if data_name == "wjsgainers": normalized_data = import_wjsgainers(raw_data)
if data_name == "ygainers": normalized_data = import_ygainers(raw_data)

assert isinstance(normalized_data['symbol'][0], str), f'Expected "symbol" to contain string type, but instead found type: {type(normalized_data["symbol"][0])}'
assert isinstance(normalized_data['price'][0], float), f'Expected "price" to contain float type, but instead found type: {type(normalized_data["price"][0])}'
assert isinstance(normalized_data['price_change'][0], float), f'Expected "price_change" to contain float type, but instead found type: {type(normalized_data["price_change"][0])}'
assert isinstance(normalized_data['price_percent_change'][0], float), f'Expected "price_percent_change" to contain float type, but instead found type: {type(normalized_data["price_percent_change"][0])}'

write_path = re.sub('[.]csv$', '_norm.csv', data_path)
normalized_data.to_csv(write_path, index=False)

print(f"\nThe data has been normalized and exported to: {write_path}\n")
