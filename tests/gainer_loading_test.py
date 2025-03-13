import os
import pytz
import pandas as pd
import pandas.api.types as ptypes
import pathlib as pl
from datetime import datetime
from bin.gainers.factory import GainerFactory

def test_gainer_download():
    factory = GainerFactory('test')
    downloader = factory.get_downloader()
    normalizer = factory.get_processor()
    
    downloader.download()

    assert any([filename == 'testgainers.csv' for filename in os.listdir('../files')])

def test_gainer_normalize_and_save():
    factory = GainerFactory('test')
    normalizer = factory.get_processor()

    normalizer.normalize()
    normalizer.save_with_timestamp()

    partial_name = f'test_gainers_{datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H')}'

    assert any([filename.startswith(partial_name) for filename in os.listdir('../files')])

def test_gainer_format():
    partial_name = f'test_gainers_{datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H')}'

    for file in os.listdir('../files'):
        if file.startswith(partial_name):
            test_data = pd.read_csv(f'../files/{file}')
            os.system(f'rm -f ../files/{file}')

    checks = [ptypes.is_numeric_dtype(test_data[cc]) for cc in ['price', 'price_change','price_percent_change']]
    checks.append(ptypes.is_string_dtype(test_data['symbol']))

    assert all(checks)
