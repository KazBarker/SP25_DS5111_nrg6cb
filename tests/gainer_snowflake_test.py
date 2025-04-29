'''
Tests the export pipeline that pushes normalized gainer files to Snowflake.
'''
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from bin.snowflake.flake_gainers import SnowflakeGainers

@pytest.mark.parametrize(
        'test_csv, expected_csv', [(
            'tests/sample_data/test_gainers_1900-01-01-09:31.csv',
            'tests/sample_data/expected_frame.csv')])
def test_get_frame(test_csv, expected_csv):
    '''
    Tests that a CSV in the expected format is parsed correctly and returned as
    a pandas dataframe.
    '''
    # GIVEN a SnowflakeGainers object, test CSV, and expected output
    snowflake = SnowflakeGainers()
    expected_df = pd.read_csv(expected_csv)

    # WHEN the parsing method is run
    parsed_df = snowflake.get_frame(test_csv)

    # THEN the resulting dataframe should match the expected output
    assert_frame_equal(expected_df, parsed_df)
