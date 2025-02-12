import os

import sys
import pandas as pd

def import_wjsgainers(wjs_data):
	assert len(wjs_data.columns) == 6, f"Expected 6 columns, found {len(wjs_data.columns)}"
	print("Found WJS Data\n")
	print(wjs_data.head(5))

def import_ygainers(y_data):
	assert len(y_data.columns) == 13, f"Expected 13 columns, found {len(y_data.columns)}"
	print("Found YFinance Data\n")
	print(y_data.head(5))


print("\n")

data_path = sys.argv[1]

try: raw_data = pd.read_csv(data_path)
except: print("There was a problem importing the data: make sure your file is a csv and check the path for errors.")

if "wjsgainers" in data_path: import_wjsgainers(raw_data)
if "ygainers" in data_path: import_ygainers(raw_data)

print("\n")
