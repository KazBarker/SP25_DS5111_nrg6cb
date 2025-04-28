'''
Module for reformatting and parsing normalized gainer files into the Snowflake gainers
tables (specified in the ERD diagram).

Intended to be used to fully recreate Snowflake tables from scratch, using the cached
gainer files.
'''
import os
import sys
import re
from pathlib import Path
import pandas as pd
import shutil
import subprocess

def get_frame(gainer_path):
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
    file = Path(gainer_path).name
    pattern = r'^[a-zA-Z]*_gainers_[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}:[0-9]{2}.csv'

    if re.fullmatch(pattern, file) is not None:
        name_data = re.sub(r'(?P<dash>-)(?=[0-9]{2}:[0-9]{2}.csv$)', r'\g<dash>_', file)
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

def parse_frame(gainer_df, project_dir):
    '''
    Takes a normalized gainers data frame with added columns "source" and "date_time"
    and parses to Snowflake/ERD format dataframes: sources, downloads, gainers, and
    gainer_details. All 4 data frames are saved to the dbt seed directory belonging to
    the project directory defined in the main clause.
    '''
    seed_dir = f'{project_dir}/seeds'

    # extract appropriate columns to data frames
    gainer_details = gainer_df.copy()
    sources = pd.DataFrame(gainer_df['source'])
    downloads = pd.DataFrame(gainer_df['date_time'])
    gainers = pd.DataFrame(gainer_df['symbol'])

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

def seed_gainers(project_dir, ii):
    '''
    Pushes the contents of the seed directory to Snowflake, then applies the incremental
    model to append the new data to the existing tables in Snowflake (unless its the
    first file in the loop, then the existing Snowflake tables are overwritten).
    The contents of the seeds directory are cleared after data is pushed to Snowflake.
    '''
    # push data to Snowflake
    seed_cmd = [
            'dbt', 'seed',
            '--project-dir', project_dir]
    
    subprocess.run(seed_cmd)

    # apply models
    for model in ['downloads', 'gainer_details', 'gainers', 'sources']:
        if ii > 0:
            model_cmd = ['dbt', 'run', '--project-dir', project_dir, '--select', model]
        else:
            model_cmd = ['dbt', 'run', '--project-dir', project_dir, '--select', model, '--full-refresh']

        subprocess.run(model_cmd)

    # remove and recreate path to project seeds
    seed_path = Path(f'{project_dir}/seeds')
    shutil.rmtree(seed_path)
    seed_path.mkdir()

if __name__ == "__main__":
    '''
    Runs the export process for a fresh rebuild of all Snowflake tables (using
    only the files within the snowflake_cache/ directory). No files are moved
    during this process.
    '''
    project_dir = 'projects/gainers'
    assert os.path.isdir(project_dir), f'{project_dir} was not found'

    directory_path = '../snowflake_cache'
    assert os.path.isdir(directory_path), f'{directory_path} was not found'

    csv_list = None

    try:
        csv_list = [ff for ff in os.listdir(directory_path) if ff.endswith('.csv')]
    except FileNotFoundError:
        print(f'{directory_path} is not a recognized directory')

    assert csv_list is not None, f'Unable to parse the files in {directory_path}'
    assert len(csv_list) > 0, f'No CSV files were found in {directory_path}'

    for ii, file in enumerate(csv_list):
        # parse and export data
        gainer_df = get_frame(f'{directory_path}/{file}')
        parse_frame(gainer_df, project_dir)
        seed_gainers(project_dir, ii)
