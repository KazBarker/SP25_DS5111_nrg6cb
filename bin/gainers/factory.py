'''
Gainer Factory
Executes commands passed from the get_gainers.py file in the home directory.
'''
from .yahoo import GainerDownloadYahoo, GainerProcessYahoo
from .wsj import GainerDownloadWSJ, GainerProcessWSJ
from .stockanalysis import GainerDownloadStockAnalysis, GainerProcessStockAnalysis
from .test import GainerDownloadTest, GainerProcessTest

class GainerFactory:
    '''
    FACTORY
    '''
    def __init__(self, choice):
        choices = ['yahoo', 'wsj', 'stockanalysis', 'test']
        assert choice in choices, f"Unrecognized gainer type {choice}"

        self.choice = choice

    def get_downloader(self):
        '''
        Retrieves the appropriate downloader method for the gainer choice passed.
        '''
        # wow this is awesome... I've always missed not having a case statement in python... I was surprised to see
        # this actually.  Looked it up and it seems it was introduced in python 3.10.  Cool.  Good use of it here!
        # also a great point for checking python versions.  If you used 3.10, and production was stuck in 3.9 there would be
        # an issue.  And that's what the github action test would have caught... 
        # learned something new today!  thanks for introducing me to the match/case, going to have to find code to use it!
        match self.choice:
            case 'yahoo':
                return GainerDownloadYahoo(
                        'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200',
                        'files/ygainers.csv',
                        'yahoo')

            case 'wsj':
                return GainerDownloadWSJ(
                        'https://www.wsj.com/market-data/stocks/us/movers',
                        'files/wsjgainers.csv',
                        'wsj')

            case 'stockanalysis':
                return GainerDownloadStockAnalysis(
                        'https://stockanalysis.com/markets/gainers/',
                        'files/stockanalysisgainers.csv',
                        'stockanalysis')

            case 'test':
                return GainerDownloadTest(
                        'none',
                        'files/testgainers.csv',
                        'test')

    def get_processor(self):
        '''
        Retrieves the appropriate processor method for the gainer choice passed.
        '''
        match self.choice:
            case 'yahoo':
                return GainerProcessYahoo(
                        'files/ygainers.csv',
                        13,
                        'yahoo')

            case 'wsj':
                return GainerProcessWSJ(
                        'files/wsjgainers.csv',
                        6,
                        'wsj')

            case 'stockanalysis':
                return GainerProcessStockAnalysis(
                        'files/stockanalysisgainers.csv',
                        8,
                        'stockanalysis')

            case 'test':
                return GainerProcessTest(
                        'files/testgainers.csv',
                        6,
                        'test')
