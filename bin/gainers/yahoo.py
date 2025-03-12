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
        self.col_count = 13
        self.name = 'yahoo'

    def normalize(self):
        print(f"normalizing {self.name} gainers...", end='')
        print('done\n')

    def save_with_timestamp(self):
        print(f'saving {self.name} gainers...', end='')
        print('done\n')

