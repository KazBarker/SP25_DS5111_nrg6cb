import os
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from io import StringIO
from .base import GainerDownload, GainerProcess 

class GainerDownloadYahoo(GainerDownload):
    '''
    DOWNLOADER (yahoo)
    Class to download ygainer html from yahoo finance, convert to a dataframe
    and save the dataframe to a csv file.
    '''
    def __init__(self):
        self.url = 'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200'
        self.out_path = '../files/ygainers.csv'
        self.name = 'yahoo'

    def download(self):
        print(f'downloading {self.name} gainers...')

        process_list = [
                'google-chrome-stable', 
                '--headless', 
                '--disable-gpu', 
                '--dump-dom', 
                '--no-sandbox', 
                '--timeout=5000',
                self.url
                ]

        # read html
        html_txt = os.popen(' '.join(process_list)).read()
        assert isinstance(html_txt, str), f'{self.name} gainers webpage filed to return text'

        # convert html to data frame list
        for ii in list(range(0, 10)):
            try:
                html_frames = pd.read_html(StringIO(html_txt))
                break
            except Exception as e:
                if ii < 10:
                    print(f'{self.name} gainers download failed, trying again...')
                else:
                    print(f'all {self.name} download attempts failed!\n')
                    print(e)
                continue

        # get data frame for gainers
        gainer_df = html_frames[0]  

        assert isinstance(gainer_df, pd.DataFrame), f'failed to build {self.name} gainers dataframe'
        if gainer_df.empty: raise Exception(f'{self.name} gainers dataframe is empty')

        # ensure the output path is empty
        os.system(f'rm -f {self.out_path}')

        # write to csv
        with open(self.out_path, 'x') as file:
            try:
                gainer_df.to_csv(self.out_path)
            except Exception as e:
                print(e)

        print('done\n')

class GainerProcessYahoo(GainerProcess):
    def __init__(self):
        self.raw_path = '../files/ygainers.csv'
        self.out_path = '../files/ygainers_norm.csv'
        self.col_count = 13
        self.name = 'yahoo'

    def normalize(self):
        '''
        Function for normalizing the ygainers.csv file. File should contain 13 
        columns, among which are columns named "Symbol", "Price", "Change", and
        "Change %".
        '''
        print(f"normalizing {self.name} gainers...", end='')
        
        # get the raw csv
        raw_csv = pd.read_csv(self.raw_path)
        assert len(raw_csv.columns) == 13, f"\nExpected 13 columns, found {len(raw_csv.columns)}\n"
        assert {
                'Symbol', 
                'Price', 
                'Change', 
                'Change %'
                }.issubset(raw_csv.columns), f'\nRaw {self.name} gainers csv is missing a required column\n'

        # fix column names
        gainers_data = raw_csv[['Symbol', 'Price', 'Change', 'Change %']].rename(
                columns={
                    'Symbol':'symbol', 
                    'Price':'price', 
                    'Change':'price_change', 
                    'Change %':'price_percent_change'
                    })
        
        # tidy up data
        gainers_data['price'] = pd.to_numeric(gainers_data['price'].str.split(' ').str[0])
        gainers_data['price_percent_change'] = pd.to_numeric(
                gainers_data['price_percent_change'].replace(r'[^0-9.]', '', regex=True))

        # write normalized data to csv
        os.system(f'rm -f {self.out_path}')
        gainers_data.to_csv(self.out_path)

        # remove raw data file
        os.system(f'rm -f {self.raw_path}')

        print('done\n')

    def save_with_timestamp(self):
        print(f'saving {self.name} gainers...', end='')
        print('done\n')

