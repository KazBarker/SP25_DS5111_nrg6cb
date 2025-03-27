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

        # initialize empty dataframe to attempt retrieval
        gainer_df = pd.DataFrame()
        check_empty = True
        ii = 0

        # loop until data is retrieved 
        while check_empty:
            # convert html to data frame list
            try:
                html_frames = pd.read_html(StringIO(html_txt))
                check_empty = False
            except ValueError:
                if ii == 1000:
                    break
                print(f'{self.name} gainers download failed, trying again...')
            except UnboundLocalError:
                if ii == 1000:
                    break
                print(f'{self.name} gainers download failed, trying again...')

            # get data frame for gainers
            gainer_df = html_frames[0]
            ii+=1

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

        print('done')

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

        count_message = f'Expected {self.col_count}, found {len(raw_csv.columns)}'
        assert len(raw_csv.columns) == self.col_count, count_message

        name_message = f'Raw {self.name} gainers csv is missing a required column'
        assert {'Symbol', 'Price', 'Change', 'Change %'
                }.issubset(raw_csv.columns), name_message

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
        symbol_type = type(self.gainers_data["symbol"][0]).__name__
        assert isinstance(self.gainers_data['symbol'][0], str),\
                f'Expected string in "symbol", instead found {symbol_type}'

        price_type = type(self.gainers_data["price"][0]).__name__
        assert isinstance(self.gainers_data['price'][0], float),\
                f'Expected float in "price", instead found {price_type}'

        price_change_type = type(self.gainers_data["price_change"][0]).__name__
        assert isinstance(self.gainers_data['price_change'][0], float),\
                f'Expected float in "price_change", instead found {price_change_type}'

        perc_change_type = type(self.gainers_data["price_percent_change"][0]).__name__
        assert isinstance(self.gainers_data['price_percent_change'][0], float), \
                f'Expected float in "price_percent_change", instead found {perc_change_type}'

        # remove raw data file
        os.system(f'rm -f {self.raw_path}')

        print('done')

    def save_with_timestamp(self):
        print(f'saving {self.name} gainers...', end='')

        count_message = f'Expected 4 columns, found {len(self.gainers_data.columns)}'
        assert len(self.gainers_data.columns) == 4, count_message

        name_message = f'{self.name} gainers data is missing a required column'
        assert {'symbol',
                'price',
                'price_change',
                'price_percent_change'
                }.issubset(self.gainers_data.columns), name_message

        # set output path with current timestamp
        timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H:%M')
        out_path = f'files/{self.name}_gainers_{timestamp}.csv'

        # save to csv
        self.gainers_data.to_csv(out_path)

        print('done')
