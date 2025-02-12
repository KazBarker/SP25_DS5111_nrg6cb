import os

import sys
import pandas as pd

data_path = sys.argv[1]

try: raw_data = pd.read_csv(data_path)
except: print("There was a problem importing the data: make sure your file is a csv and check the path for errors.")
