'''
Gainer Factory Yahoo Methods

Includes methods for download of html yahoo gainers data, and for normalization
and saving of data to a timestamped csv file.
'''
import os
from datetime import datetime
from io import StringIO
import pytz
import pandas as pd
from .base import GainerDownload, GainerProcess

class GainerDownloadYahoo(GainerDownload):
    '''
    DOWNLOADER (yahoo)
    Class to download ygainer html from yahoo finance, convert to a dataframe
    and save the dataframe to a csv file.
    '''
    def __init__(self, url, out_path, name):
        self.url = url
        self.out_path = out_path
        self.name = name

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

        assert isinstance(gainer_df, pd.DataFrame), f'failed to build {self.name} gainers dataframe'
        if gainer_df.empty:
            raise ValueError(f'{self.name} gainers dataframe is empty')

        # ensure the output path is empty
        os.system(f'rm -f {self.out_path}')

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

class GainerProcessYahoo(GainerProcess):
    '''
    PROCESSOR (yahoo)
    Normalizes the yahoo gainers data and saves to a timestamped csv file - the 
    original raw csv (ygainers.csv) is removed after normalization.
    '''
    def __init__(self, raw_path, col_count, name):
        self.raw_path = raw_path
        self.gainers_data = 'none'
        self.col_count = col_count
        self.name = name

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
        assert {'Symbol',
                'Price', 
                'Change', 
                'Change %'
                }.issubset(raw_csv.columns), f'\nRaw {
        self.name} gainers csv is missing a required column\n'

        # fix column names
        self.gainers_data = raw_csv[['Symbol', 'Price', 'Change', 'Change %']].rename(
                columns={'Symbol':'symbol',
                         'Price':'price',
                         'Change':'price_change',
                         'Change %':'price_percent_change'})

        # tidy up data
        self.gainers_data['price'] = pd.to_numeric(self.gainers_data['price'].str.split(' ').str[0])
        self.gainers_data['price_percent_change'] = pd.to_numeric(
                self.gainers_data['price_percent_change'].replace(r'[^0-9.]', '', regex=True))

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
        out_path = f'../files/{self.name}_gainers_{timestamp}.csv'

        # save to csv
        self.gainers_data.to_csv(out_path)

        print('done\n')
