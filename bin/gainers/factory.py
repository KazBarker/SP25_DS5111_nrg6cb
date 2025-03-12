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

