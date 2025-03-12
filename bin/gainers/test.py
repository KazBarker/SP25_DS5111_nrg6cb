import os
import pytz
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
from io import StringIO
from .base import GainerDownload, GainerProcess

class GainerDownloadTest(GainerDownload):
    '''
    DOWNLOADER (test)
    '''
    def __init__(self):
        self.url = 'none'
        self.out_path = '../files/testgainers.csv'
        self.name = 'test'

    def download(self):
        print(f'downloading {self.name} gainers...')

        # get fake data frame 
        gainer_df = pd.DataFrame(np.random.randint(0, 1000, size=(20,5)),
                                 columns=['C1', 'C2', 'C3', 'C4', 'C5'])

        # ensure the output path is empty
        os.system(f'rm -f {self.out_path}')

        assert isinstance(gainer_df, pd.DataFrame), f'failed to build {self.name} dataframe'
        if gainer_df.empty: raise Exception(f'{self.name} dataframe is empty')

        # write to csv
        with open(self.out_path, 'x') as file:
            try:
                gainer_df.to_csv(self.out_path)
            except Exception as e:
                print(e)

        print('done\n')

class GainerProcessTest(GainerProcess):
    '''
    PROCESSOR (test)
    Normalizes the test gainers data - the original raw csv (testgainers.csv) is removed
    after normalization.
    '''
    def __init__(self):
        self.raw_path = '../files/testgainers.csv'
        self.out_path = '../files/norm_testgainers.csv'
        self.col_count = 6
        self.name = 'test'

    def normalize(self):
        '''
        Function for normalizing the testgainers.csv file. File must contain 5 columns and
        must include columns with names: "C1", "C2", "C3", and "C4".
        '''
        print(f'normalizing {self.name} gainers data...', end='')

        # get the raw csv
        raw_csv = pd.read_csv(self.raw_path)

        assert len(raw_csv.columns) == self.col_count, f"\nExpected {self.col_count} columns, found {len(raw_csv.columns)}\n"
        assert {
                'C1',
                'C2',
                'C3',
                'C4'
                }.issubset(raw_csv.columns), f'\nRaw {self.name} gainers csv is missing a required column\n'
        
        # fix column names
        self.gainers_data = raw_csv[['C1', 'C2', 'C3', 'C4']].rename(
                columns={
                    'C1':'symbol', 
                    'C2':'price', 
                    'C3':'price_change', 
                    'C4':'price_percent_change'
                    })

        # remove raw data file
        os.system(f'rm -f {self.raw_path}')

        print('done\n')

    def save_with_timestamp(self):
        print(f'saving {self.name} gainers...', end='')
        assert len(self.gainers_data.columns) == 4, f'\nExpected 4 columns, found {len(self.gainers_data.columns)}\n'
        assert {
                'symbol',
                'price',
                'price_change',
                'price_percent_change'
                }.issubset(self.gainers_data.columns), f'\n{self.name} gainers data is missing a required column\n'

        # set output path with current timestamp
        timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H:%M')
        self.out_path = f'../files/{self.name}_gainers_{timestamp}.csv'

        # save to csv
        self.gainers_data.to_csv(self.out_path)
        
        print('done\n')

