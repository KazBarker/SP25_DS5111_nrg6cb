'''
Gainer Factory methods for Stock Analysis data. Includes classes for downloading from
a url and for normalizing and saving as a timestamped csv file.
'''
import os
from datetime import datetime
from io import StringIO
import pytz
import pandas as pd
from .base import GainerDownload, GainerProcess

class GainerDownloadStockAnalysis(GainerDownload):
    '''
    DOWNLOADER
    Class to download html, convert to a dataframe and save the dataframe to a csv file.
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
                '--timeout=15000',
                self.url
                ]

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
                check_empty = False
                html_frames = pd.read_html(StringIO(html_txt))
            except ValueError:
                if ii == 100000:
                    break
                print(f'{self.name} gainers download failed, trying again...')
            except UnboundLocalError:
                if ii == 100000:
                    break
                print(f'{self.name} gainers download failed, trying again...')

            # get data frame for gainers
            gainer_df = html_frames[0]
            ii+=1

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

        print('done')

class GainerProcessStockAnalysis(GainerProcess):
    '''
    PROCESSOR
    Normalizes the gainers data - the original raw csv is removed after normalization.
    '''
    def __init__(self, raw_path, col_count, name):
        self.raw_path = raw_path
        self.col_count = col_count
        self.name = name

    def normalize(self):
        '''
        Function for normalizing the wsjgainers.csv file. File must contain 6 columns and
        must include columns with names: "Unnamed: 0", "Last", "Chg", and "% Chg".
        '''
        print(f'normalizing {self.name} gainers...', end='')

        # get the raw csv
        raw_csv = pd.read_csv(self.raw_path)

        count_message = f'Expected {self.col_count} columns, found {len(raw_csv.columns)}'
        assert len(raw_csv.columns) == self.col_count, count_message

        name_message = f'Raw {self.name} gainers csv is missing a required column'
        assert {'Symbol',
                '% Change',
                'Stock Price'
                }.issubset(raw_csv.columns), name_message

        # fix column names
        self.gainers_data = raw_csv[['Symbol', '% Change', 'Stock Price']].rename(
                columns={
                    'Symbol': 'symbol', 
                    'Stock Price':'price', 
                    '% Change':'price_percent_change'
                    })

        # tidy up data
        self.gainers_data['price_percent_change'] = self.gainers_data[
                'price_percent_change'].replace(
                        r'%', '', regex=True).replace(
                                r' ', '', regex=True).replace(
                                        r',', '', regex=True).astype(float)

        self.gainers_data['price_change'] = self.gainers_data['price'] - (
                self.gainers_data['price'] / (1 + (self.gainers_data['price_percent_change'] / 100))
                )

        self.gainers_data['price_change'] = self.gainers_data['price_change'].round(2)

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

        names_message = f'{self.name} gainers data is missing a required column'
        assert {'symbol',
                'price',
                'price_change',
                'price_percent_change'
                }.issubset(self.gainers_data.columns), names_message

        # set output path with current timestamp
        timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H:%M')
        out_path = f'files/{self.name}_gainers_{timestamp}.csv'

        # save to csv
        self.gainers_data.to_csv(out_path, index=False)

        print('done')
