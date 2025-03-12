import os
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from io import StringIO

# FACTORY
class GainerFactory:
    def __init__(self, choice):
        assert choice in ['yahoo', 'wsj', 'test'], f"Unrecognized gainer type {choice}"
        self.choice = choice 

    def get_downloader(self):
        match self.choice:
            case 'yahoo':
                return GainerDownloadYahoo()

            case 'wsj':
                return GainerDownloadWSJ()

            case 'test':
                return GainerDownloadTest()

    def get_processor(self):
        # trigger off url to return correct downloader
        match self.choice:
            case 'yahoo':
                return GainerProcessYahoo()

            case 'wsj':
                return GainerProcessWSJ()

            case 'test':
                return GainerProcessTest()

# DOWNLOADER
class GainerDownload(ABC):
    def __init__(self):
        self.url = url
        self.out_path = out_path
        self.name = data_name

    @abstractmethod
    def download(self):
        pass

class GainerDownloadYahoo(GainerDownload):
    def __init__(self):
        self.url = 'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200'
        self.out_path = '../../../files/ygainers.csv'
        self.name = 'yahoo'

    def download(self):
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
        html_frames = pd.read_html(StringIO(html_txt))

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

        print(f'downloading {self.name} gainers')

class GainerDownloadWSJ(GainerDownload):
    def __init__(self):
        self.url = 'https://www.wsj.com/market-data/stocks/us/movers'
        self.out_path = '../../../files/wsjgainers.csv'
        self.name = 'wsj'

    def download(self):
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
        html_frames = pd.read_html(StringIO(html_txt))

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

        print(f'downloading {self.name} gainers')

class GainerDownloadTest(GainerDownload):
    def __init__(self):
        self.url = 'none'
        self.out_path = '../../../files/testgainers.csv'
        self.name = 'test'

    def download(self):
        # get fake data frame 
        gainer_df = pd.DataFrame(np.random.randint(0, 1000, size=(20,5)),
                                 columns=['C1', 'C2', 'C3', 'C4', 'C5'])

        assert isinstance(gainer_df, pd.DataFrame), f'failed to build {self.name} dataframe'
        if gainer_df.empty: raise Exception(f'{self.name} dataframe is empty')

        # ensure the output path is empty
        os.system(f'rm -f {self.out_path}')

        # write to csv
        with open(self.out_path, 'x') as file:
            try:
                gainer_df.to_csv(self.out_path)
            except Exception as e:
                print(e)

        print(f'downloading {self.name} gainers')

# PROCESSORS 
class GainerProcess(ABC):
    def __init__(self):
        self.path = path

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def save_with_timestamp(self):
        pass

class GainerProcessYahoo(GainerProcess):
    def __init__(self):
        pass

    def normalize(self):
        print("Normalizing yahoo gainers")

    def save_with_timestamp(self):
        print("Saving yahoo gainers")

class GainerProcessWSJ(GainerProcess):
    def __init__(self):
        pass

    def normalize(self):
        print("Normalizing WSJ gainers")

    def save_with_timestamp(self):
        print("Saving WSJ gainers")

class GainerProcessTest(GainerProcess):
    def __init__(self):
        pass

    def normalize(self):
        print("Normalizing Test gainers")

    def save_with_timestamp(self):
        print("Saving Test gainers")

# TEMPLATE
class ProcessGainer:
    def __init__(self, gainer_downloader, gainer_normalizer):
        self.downloader = gainer_downloader
        self.normalizer = gainer_normalizer

    def _download(self):
        self.downloader.download()

    def _normalize(self):
        self.normalizer.normalize()

    def _save_to_file(self):
        self.normalizer.save_with_timestamp()

    def process(self):
        self._download()
        self._normalize()
        self._save_to_file()

if __name__=="__main__":
    # Our sample main file would look like this
    import sys
   
    # Make our selection, 'one' choice
    choice = sys.argv[1]

    # let our factory get select the family of objects for processing
    factory = GainerFactory(choice)
    downloader = factory.get_downloader()
    normalizer = factory.get_processor()

    # create our process
    runner = ProcessGainer(downloader, normalizer)
    runner.process()




