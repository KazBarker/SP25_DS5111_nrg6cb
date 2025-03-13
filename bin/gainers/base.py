'''
Base class for Gainer Factory methods. Includes patterns for download
and for processing (normalization and saving to a timestamped file.)
'''
from abc import ABC, abstractmethod

class GainerDownload(ABC):
    '''
    DOWNLOADER
    Pattern for downloading gainer data from an html file and saving
    to a (temporary) csv file for processing.
    '''
    def __init__(self, url, out_path, name):
        self.url = url
        self.out_path = out_path
        self.name = name

    @abstractmethod
    def download(self):
        '''
        Here the raw html will be extracted from the url defined above,
        converted to a dataframe, and saved to a temporary csv file.
        '''
        pass

class GainerProcess(ABC):
    '''
    PROCESSOR
    Pattern for taking a raw csv file of gainer data and converting
    to a standard column and data format, and for saving the normalized
    data to a timestamped csv file.
    '''
    def __init__(self, raw_path, col_count, name):
        self.raw_path = raw_path
        self.gainers_data = 'none'
        self.col_count = col_count
        self.name = name

    @abstractmethod
    def normalize(self):
        '''
        Here the raw csv file from GainerDownload will be converted to
        a standardized format.
        '''
        pass

    @abstractmethod
    def save_with_timestamp(self):
        '''
        Here the standardized data will be written to a final csv file,
        which includes a timestamp in the file name corresponding to the
        time at which the file was saved.
        '''
        pass
