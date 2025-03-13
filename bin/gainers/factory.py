'''
Gainer Factory
Executes commands passed from the get_gainers.py file in the home directory.
'''
from .yahoo import GainerDownloadYahoo, GainerProcessYahoo
from .wsj import GainerDownloadWSJ, GainerProcessWSJ
from .test import GainerDownloadTest, GainerProcessTest

class GainerFactory:
    '''
    FACTORY
    '''
    def __init__(self, choice):
        assert choice in ['yahoo', 'wsj', 'test'], f"Unrecognized gainer type {choice}"
        self.choice = choice

    def get_downloader(self):
        '''
        Retrieves the appropriate downloader method for the gainer choice passed.
        '''
        match self.choice:
            case 'yahoo':
                return GainerDownloadYahoo(
                        'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200',
                        '../files/ygainers.csv',
                        'yahoo')

            case 'wsj':
                return GainerDownloadWSJ(
                        'https://www.wsj.com/market-data/stocks/us/movers',
                        '../files/wsjgainers.csv',
                        'wsj')

            case 'test':
                return GainerDownloadTest(
                        'none',
                        '../files/testgainers.csv',
                        'test')

    def get_processor(self):
        '''
        Retrieves the appropriate processor method for the gainer choice passed.
        '''
        match self.choice:
            case 'yahoo':
                return GainerProcessYahoo(
                        '../files/ygainers.csv',
                        13,
                        'yahoo')

            case 'wsj':
                return GainerProcessWSJ(
                        '../files/wsjgainers.csv',
                        6,
                        'wsj')

            case 'test':
                return GainerProcessTest(
                        '../files/testgainers.csv',
                        6,
                        'test')
