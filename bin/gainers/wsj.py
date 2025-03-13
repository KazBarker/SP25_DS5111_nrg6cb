'''
Gainer Factory methods for WSJ data. Includes classes for downloading from
a url and for normalizing and saving as a timestamped csv file.
'''
import os
import pytz
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
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
        for ii in list(range(0, 11)):
            try:
                html_frames = pd.read_html(StringIO(html_txt))
                break
            except UnboundLocalError:
                if ii < 10:
                    print(f'{self.name} gainers download failed, trying again...')
                    continue
                print(f'all {self.name} download attempts failed!\n')

        # get data frame for gainers
        gainer_df = html_frames[0]

        # ensure the output path is empty
        os.system(f'rm -f {self.out_path}')

        assert isinstance(gainer_df, pd.DataFrame), f'failed to build {self.name} dataframe'

        if gainer_df.empty:
            raise ValueError(f'{self.name} dataframe is empty')

        # write to csv
        with open(self.out_path, 'x', encoding='utf-8') as file:
            try:
                gainer_df.to_csv(self.out_path)
            except FileExistsError:
                print(f"Error: The file '{self.out_path}' already exists.")
            except PermissionError:
                print(f"Error: Permission denied when trying to write to '{self.out_path}'.")
            except OSError as e:
                print(f"OS error occurred: {e}")

        print('done\n')

class GainerProcessWSJ(GainerProcess):
    '''
    PROCESSOR (wsj)
    Normalizes the WSJ gainers data - the original raw csv (wsjgainers.csv) is removed
    after normalization.
    '''
    def __init__(self):
        self.raw_path = '../files/wsjgainers.csv'
        self.col_count = 6
        self.name = 'wsj'

    def normalize(self):
        '''
        Function for normalizing the wsjgainers.csv file. File must contain 6 columns and
        must include columns with names: "Unnamed: 0", "Last", "Chg", and "% Chg".
        '''
        print(f'normalizing {self.name} gainers...', end='')

        # get the raw csv
        raw_csv = pd.read_csv(self.raw_path)

        assert len(raw_csv.columns) == self.col_count, f"\nExpected {
        self.col_count} columns, found {len(raw_csv.columns)}\n"

        assert {
                'Unnamed: 0',
                'Last',
                'Chg',
                '% Chg'
                }.issubset(raw_csv.columns), f'\nRaw {
        self.name} gainers csv is missing a required column\n'

        # fix column names
        self.gainers_data = raw_csv[['Unnamed: 0', 'Last', 'Chg', '% Chg']].rename(
                columns={
                    'Unnamed: 0':'symbol', 
                    'Last':'price', 
                    'Chg':'price_change', 
                    '% Chg':'price_percent_change'
                    })

        # tidy up data
        self.gainers_data['symbol'] = self.gainers_data['symbol'].replace(
                r'.*[(]', '', regex=True).replace(r'[)].*', '', regex=True)

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

        assert {
                'symbol',
                'price',
                'price_change',
                'price_percent_change'
                }.issubset(self.gainers_data.columns), f'\n{
        self.name} gainers data is missing a required column\n'

        # set output path with current timestamp
        timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H:%M')
        out_path = f'../files/{self.name}_gainers_{timestamp}.csv'

        # save to csv
        self.gainers_data.to_csv(out_path)

        print('done\n')
