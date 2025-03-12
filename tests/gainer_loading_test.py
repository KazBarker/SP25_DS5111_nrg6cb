import os
import pytz
import pandas as pd
import pathlib as pl
from datetime import datetime
from bin.gainers.factory import GainerFactory

def test_gainer_download():
    factory = GainerFactory('test')
    downloader = factory.get_downloader()
    normalizer = factory.get_processor()
    
    downloader.download()

    assert any([filename == 'testgainers.csv' for filename in os.listdir('../files')])

def test_gainer_normalize():
    factory = GainerFactory('test')
    normalizer = factory.get_processor()

    normalizer.normalize()
    normalizer.save_with_timestamp()

    partial_name = f'test_gainers_{datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H')}'

    assert any([filename.startswith(partial_name) for filename in os.listdir('../files')])

'''
        # set output path with current timestamp
        timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H:%M')
        out_path = f'../files/{self.name}_gainers_{timestamp}.csv'


    assert pl.Path(
    downloaded = pd.read_csv('../../files/
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))




def test_gainer_normalize():
    normalizer.normalize()
    normalizer.save_with_timestamp()

   ''' 
