'''
Gainer Factory Test Methods

Includes methods for simulated download (i.e. random generation) of test data, and for
normalization and saving of test data to a timestamped csv file.
'''
import os
from datetime import datetime
import pytz
import numpy as np
import pandas as pd
from .base import GainerDownload, GainerProcess

class GainerDownloadTest(GainerDownload):
    '''
    DOWNLOADER (test)
    '''
    def __init__(self, url, out_path, name):
        self.url = url
        self.out_path = out_path
        self.name = name

    def download(self):
        print(f'downloading {self.name} gainers...')
        
        # initialize empty dataframe to attempt retrieval
        gainer_df = pd.DataFrame()
        ii = 0

        # loop until data is retrieved 
        while gainer_df.empty and ii < 50:
            # get fake data frame
            if ii > 20: 
                gainer_df = pd.DataFrame(np.random.randint(0, 128, size=(20,5)).astype(float),
                                         columns=['C1', 'C2', 'C3', 'C4', 'C5'])
            ii+=1

        gainer_df['C1'] = [chr(int(xx)) for xx in gainer_df['C1']]

        # ensure the output path is empty
        os.system(f'rm -f {self.out_path}')

        assert isinstance(gainer_df, pd.DataFrame), f'failed to build {self.name} dataframe'
        if gainer_df.empty:
            raise ValueError(f'{self.name} dataframe is empty')

        # write to csv
        try:
            gainer_df.to_csv(self.out_path)
        except FileExistsError:
            print(f"Error: The file '{self.out_path}' already exists.")
        except PermissionError:
            print(f"Error: Permission denied when trying to write to '{self.out_path}'.")
        except OSError as e:
            print(f"OS error occurred: {e}")

        print('done\n')

class GainerProcessTest(GainerProcess):
    '''
    PROCESSOR (test)
    Normalizes the test gainers data - the original raw csv (testgainers.csv) is removed
    after normalization.
    '''
    def __init__(self, raw_path, col_count, name):
        self.raw_path = raw_path
        self.raw_csv = 'none'
        self.col_count = col_count
        self.name = name

    def normalize(self):
        '''
        Function for normalizing the testgainers.csv file. File must contain 5 columns and
        must include columns with names: "C1", "C2", "C3", and "C4".
        '''
        print(f'normalizing {self.name} gainers ...', end='')

        # get raw csv
        self.gainers_data = pd.read_csv(self.raw_path)

        assert len(self.gainers_data.columns) == self.col_count, f"\nExpected {
        self.col_count} columns, found {len(self.gainers_data.columns)}\n"

        assert {'C1',
                'C2',
                'C3',
                'C4'
                }.issubset(self.gainers_data.columns), f'\nRaw {
        self.name} gainers csv is missing a required column\n'

        # fix column names
        self.gainers_data = self.gainers_data[['C1', 'C2', 'C3', 'C4']].rename(
                columns={'C1':'symbol',
                         'C2':'price',
                         'C3':'price_change',
                         'C4':'price_percent_change'})

        # check normalized data format
        assert isinstance(self.gainers_data['symbol'][0], str),\
                f'Expected string in "symbol", instead found {
                type(self.gainers_data["symbol"][0]).__name__}'

        assert isinstance(self.gainers_data['price'][0], float),\
                f'Expected float in "price", instead found {
                type(self.gainers_data["price"][0]).__name__}'

        assert isinstance(self.gainers_data['price_change'][0], float),\
                f'Expected float in "price_change", instead found {
                type(self.gainers_data["price_change"][0]).__name__}'

        assert isinstance(self.gainers_data['price_percent_change'][0], float), \
                f'Expected float in "price_percent_change", instead found {
                type(self.gainers_data["price_percent_change"][0]).__name__}'

        # remove raw data file
        os.system(f'rm -f {self.raw_path}')

        print('done\n')

    def save_with_timestamp(self):
        print(f'saving {self.name} gainers...', end='')

        assert len(self.gainers_data.columns) == 4, f'\nExpected 4 columns, found {
        len(self.gainers_data.columns)}\n'

        assert {'symbol',
                'price',
                'price_change',
                'price_percent_change'
                }.issubset(self.gainers_data.columns), f'\n{
        self.name} gainers data is missing a required column\n'

        # set output path with current timestamp
        timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H:%M')
        out_path = f'files/{self.name}_gainers_{timestamp}.csv'

        # save to csv
        self.gainers_data.to_csv(out_path)

        print('done\n')
