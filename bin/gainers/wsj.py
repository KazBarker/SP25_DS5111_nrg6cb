import os
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from io import StringIO
from .base import GainerDownload, GainerProcess

class GainerDownloadWSJ(GainerDownload):
    '''
    DOWNLOADER (wsj)
    Class to download ygainer html from yahoo finance, convert to a dataframe
    and save the dataframe to a csv file.
    '''
    def __init__(self):
        self.url = 'https://www.wsj.com/market-data/stocks/us/movers'
        self.out_path = '../files/wsjgainers.csv'
        self.name = 'wsj'

    def download(self):
        print(f'downloading {self.name} gainers...')

        process_list = [
                'google-chrome-stable',
                '--headless',
                '--disable-gpu',
                '--dump-dom',
                '--no-sandbox',
                '--timeout=15000',
                self.url
                ]

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

class GainerProcessWSJ(GainerProcess):
    '''
    PROCESSOR (wsj)
    Normalizes the WSJ gainers data - the original raw csv (wsjgainers.csv) is removed
    after normalization.
    '''
    def __init__(self):
        self.raw_path = '../files/wsjgainers.csv'
        self.out_path = '../files/wsjgainers_norm.csv'
        self.col_count = 6
        self.name = 'wsj'

    def normalize(self):
        '''
        Function for normalizing the wsjgainers.csv file. File must contain 6 columns and
        must include columns with names: "Unnamed: 0", "Last", "Chg", and "% Chg".
        '''
        print(f'normalizing {self.name} gainers data...', end='')

        # get the raw csv
        raw_csv = pd.read_csv(self.raw_path)
        assert len(raw_csv.columns) == self.col_count, f"\nExpected {self.col_count} columns, found {len(raw_csv.columns)}\n"
        assert {
                'Unnamed: 0',
                'Last',
                'Chg',
                '% Chg'
                }.issubset(raw_csv.columns), f'\nRaw {self.name} gainers csv is missing a required column\n'
        
        # fix column names
        gainers_data = raw_csv[['Unnamed: 0', 'Last', 'Chg', '% Chg']].rename(
                columns={
                    'Unnamed: 0':'symbol', 
                    'Last':'price', 
                    'Chg':'price_change', 
                    '% Chg':'price_percent_change'
                    })

        # tidy up data
        gainers_data['symbol'] = gainers_data['symbol'].replace(
                r'.*[(]', '', regex=True).replace(r'[)].*', '', regex=True)
        
        # write normalized data to csv
        os.system(f'rm -f {self.out_path}')
        gainers_data.to_csv(self.out_path)
        
        # remove raw data file
        os.system(f'rm -f {self.raw_path}')

        print('done\n')

    def save_with_timestamp(self):
        print(f'saving {self.name} gainers...', end='')
        print('done\n')

