'''
Tests for the Gainer Factory

These tests simulate the gainer factory process without an html download. They
rely on the "test" methods, for which random data is generated - this random
data is then processed identically to other gainers data (only missing the html
step)
'''
import os
from datetime import datetime
import pytz
import pandas as pd
import pandas.api.types as ptypes
from bin.gainers.factory import GainerFactory

def test_gainer_download():
    '''
    Checks that the Gainer Factory saves a csv file when downloader.download() is
    called.
    '''
    # GIVEN a GainerFactory test object
    factory = GainerFactory('test')

    # WHEN the downloeader is instantiated and run
    downloader = factory.get_downloader()
    downloader.download()

    # THEN a testgainers.csv file will have been created in the files/ directory
    assert any(iter(filename == 'testgainers.csv' for filename in os.listdir('files')))

def test_gainer_normalize_and_save():
    '''
    Checks that the Gainer Factory creates a timestamped csv file when the 
    normalizer methods are called.
    '''
    # GIVEN a GainerFactory test object
    factory = GainerFactory('test')
    normalizer = factory.get_processor()

    # WHEN the normalizer is instantiated and run
    normalizer.normalize()
    normalizer.save_with_timestamp()

    # THEN a file beginning with test_gainers_[timestamp] will exist in filea/
    timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H')
    partial_name = f'test_gainers_{timestamp}'

    assert any(iter(filename.startswith(partial_name) for filename in os.listdir('files')))

def test_gainer_format():
    '''
    Checks that the Gainer Factory has created a timestamped csv file with the correct
    column formats. This final test removes the testing csv file when executed.
    '''
    # GIVEN a gainer test file beginning with test_gainers_[timestamp]
    timestamp = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d-%H')
    partial_name = f'test_gainers_{timestamp}'

    # WHEN the file is read into a pandas dataframe
    for file in os.listdir('files'):
        if file.startswith(partial_name):
            test_data = pd.read_csv(f'files/{file}')
            os.system(f'rm -f files/{file}')

    # THEN 3 columns will be numeric and 1 will be a string (as specified)
    checks = [ptypes.is_numeric_dtype(test_data[cc]) for cc in
              ['price', 'price_change','price_percent_change']]

    checks.append(ptypes.is_string_dtype(test_data['symbol']))

    assert all(checks)
