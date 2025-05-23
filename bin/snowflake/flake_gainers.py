'''
Module for reformatting and parsing normalized gainer files into the Snowflake gainers
tables (specified in the ERD diagram).

Intended to add any new gainers files from the files/ directory to Snowflake (will not
overwrite any existing Snowflake tables). New files will be moved to the cache outside
the GitHub repo after export.
'''
import os
import sys
import re
import shutil
import subprocess
from pathlib import Path
import pandas as pd

class SnowflakeGainers:
    '''
    Methods for exporting normalized gainer files to Snowflake.
    '''
    def get_frame(self, gainer_path):
        '''
        Takes a normalized gainers CSV file (by file path), extracts timestamp and 
        data source from the file name, and loads file contents into a pandas dataframe.
        Returns a pandas dataframe with the normalized gainers file, augmented with
        combined timestamp and data source information.
        '''
        # read normalized gainers file to pandas dataframe
        gainers_df = pd.read_csv(gainer_path)
        assert isinstance(gainers_df, pd.DataFrame), '{gainer_path} could not be imported.'

        # extract source and timestamp info
        gainer_file = Path(gainer_path).name
        pattern = r'^[a-zA-Z]*_gainers_[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}:[0-9]{2}.csv'

        if re.fullmatch(pattern, gainer_file) is not None:
            name_data = re.sub(r'(?P<dash>-)(?=[0-9]{2}:[0-9]{2}.csv$)', r'\g<dash>_', gainer_file)
            name_data = name_data.replace("-", "").replace(":", "").replace("_gainers_", "_")
            source = re.sub(r'_.*', '', name_data)
            date_time = name_data.replace(source, '').replace('.csv', '')
            date_time = re.sub(r'^_', '', date_time)
        else:
            raise ValueError("The file provided did not match the expected naming convention.")

        # add source and timestamp to dataframe column
        gainers_df['source'] = source
        gainers_df['date_time'] = date_time

        return gainers_df

    def parse_frame(self, gainer_frame, project_path):
        '''
        Takes a normalized gainers data frame with added columns "source" and "date_time"
        and parses to Snowflake/ERD format dataframes: sources, downloads, gainers, and
        gainer_details. All 4 data frames are saved to the dbt seed directory belonging to
        the project directory defined in the main clause.
        '''
        seed_dir = f'{project_path}/seeds'

        # extract appropriate columns to data frames
        gainer_details = gainer_frame.copy()
        sources = pd.DataFrame(gainer_frame['source'])
        downloads = pd.DataFrame(gainer_frame['date_time'])
        gainers = pd.DataFrame(gainer_frame['symbol'])

        # parse downloads contents
        pattern = r'(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})_(?P<time>[0-9]{4})'

        downloads['year'] = downloads['date_time'].str.replace(pattern, r'\g<year>', regex=True)
        downloads['month'] = downloads['date_time'].str.replace(pattern, r'\g<month>', regex=True)
        downloads['day'] = downloads['date_time'].str.replace(pattern, r'\g<day>', regex=True)
        downloads['time'] = downloads['date_time'].str.replace(pattern, r'\g<time>', regex=True)

        # ensure the seed directory is empty
        seed_path = Path(seed_dir)

        if seed_path.exists():
            shutil.rmtree(seed_path)

        seed_path.mkdir()

        # write frames to csv files in the seed directory
        gainer_details.to_csv(f'{seed_dir}/gainer_details_seed.csv', index=False)
        sources.to_csv(f'{seed_dir}/sources_seed.csv', index=False)
        downloads.to_csv(f'{seed_dir}/downloads_seed.csv', index=False)
        gainers.to_csv(f'{seed_dir}/gainers_seed.csv', index=False)

    def seed_gainers(self, project_path):
        '''
        Pushes the contents of the seed directory to Snowflake, then applies the incremental
        model to append the new data to the existing tables in Snowflake (unless its the
        first file in the loop, then the existing Snowflake tables are overwritten).
        The contents of the seeds directory are cleared after data is pushed to Snowflake.
        '''
        # push data to Snowflake
        seed_cmd = ['dbt', 'seed', '--project-dir', project_path]

        try:
            subprocess.run(seed_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f'dbt seed failed to run. Exit code: {e.returncode}')

        # apply models
        for model in ['downloads', 'gainer_details', 'gainers', 'sources']:
            model_cmd = ['dbt', 'run', '--project-dir', project_path, '--select', model]

            try:
                subprocess.run(model_cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f'dbt run failed to execute. Exit code: {e.returncode}')

        # remove and recreate path to project seeds
        seed_path = Path(f'{project_path}/seeds')
        shutil.rmtree(seed_path)
        seed_path.mkdir()

if __name__ == "__main__":
    PROJECT_DIR = 'projects/gainers_export'
    assert os.path.isdir(PROJECT_DIR), f'{PROJECT_DIR} was not found'

    directory_path = sys.argv[1]
    assert os.path.isdir(directory_path), f'{directory_path} is invalid'

    CSV_LIST = None

    try:
        CSV_LIST = [ff for ff in os.listdir(directory_path) if ff.endswith('.csv')]
    except FileNotFoundError:
        print(f'{directory_path} is not a recognized directory')

    assert CSV_LIST is not None, f'Unable to parse the files in {directory_path}'
    assert len(CSV_LIST) > 0, f'No CSV files were found in {directory_path}'

    snowflake = SnowflakeGainers()

    for file in CSV_LIST:
        # parse and export data
        gainer_df = snowflake.get_frame(f'{directory_path}/{file}')
        snowflake.parse_frame(gainer_df, PROJECT_DIR)
        snowflake.seed_gainers(PROJECT_DIR)

        # move file to the cache location
        CACHE_DIR = '../snowflake_cache/'

        if not Path(CACHE_DIR).exists():
            Path(CACHE_DIR).mkdir()

        shutil.move(f'{directory_path}/{file}', os.path.join(CACHE_DIR, os.path.basename(file)))
