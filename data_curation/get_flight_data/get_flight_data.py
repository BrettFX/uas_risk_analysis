__author__ = 'Brett Allen (brettallen777@gmail.com)'

from pyopensky.config import opensky_config_dir
from pyopensky.trino import Trino
import pandas as pd
import awswrangler as wr
from glob import glob
import os
import datetime
from tqdm import tqdm
import argparse
import json
from uuid import uuid4

DEFAULT_PROFILE = 'endurasoft-dev'
DEFAULT_CONFIG = 'default.env'
DEFAULT_CHECKPOINT_DIR = 'checkpoints'
SESSION_ID = str(uuid4())

# Ensure connection to s3
os.environ['AWS_DEFAULT_PROFILE'] = DEFAULT_PROFILE

parser = argparse.ArgumentParser(
    prog = 'get_flight_data.py',
    description = 'Download flight profiles, flight track points, and flight messages data from Opensky-Network via API access.',
)

parser.add_argument('--session_id', help='Optionally start back up from where a previous session left off by providing the session id of the checkpoint path.')

def save_checkpoint(session_state: dict, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(session_state, f, indent=2, default=str)

def load_checkpoint(path: str) -> dict:
    session_state = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            session_state = json.load(f)
    return session_state

def get_track_points(trino: Trino, airports: set, **kwargs):
    # TODO Implement approach for loading previous session state
    output_path = kwargs['output_path']
    if not output_path.strip().lower().endswith('track-points'):
        output_path = os.path.join(output_path, 'track-points')

    flights_per_request = kwargs['flights_per_request']
    hours_interval = kwargs['hours_interval']

    start_datetime = datetime.datetime.strptime(kwargs['start'], '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.datetime.strptime(kwargs['end'], '%Y-%m-%d %H:%M:%S')

    current_datetime = end_datetime # start_datetime
    extract_num = 0
    date_diff = end_datetime - start_datetime
    days, seconds = date_diff.days, date_diff.seconds
    hours = days * 24 + seconds // 3600
    num_iters = hours // hours_interval
    if hours % hours_interval != 0:
        num_iters += 1

    with tqdm(total=num_iters) as pbar:
        # Work backwards so that latest data is prioritized first
        while current_datetime > start_datetime:
            start = current_datetime - datetime.timedelta(hours=hours_interval)

            if start < start_datetime:
                # print(f'{start} is less than {start_datetime}')
                start = start_datetime

            stop = current_datetime
            pbar.set_description(f'Obtaining Extraction {extract_num+1} of {num_iters}: {start} to {stop}', refresh=True)
            # print(f'Obtaining Extraction {extract_num+1} of {num_iters}: {start} to {stop}')

            # Make request for flight profiles
            flight_profiles = trino.flightlist(
                start=start,
                stop=stop
            )
            
            # Filter flight profiles where departure and arrival are known and belong in the airports list
            filtered_profiles = flight_profiles[(flight_profiles['departure'].isin(airports)) & (flight_profiles['arrival'].isin(airports))]

            # Filter by random sample based on flights per request. If total number of track points is less than flights per request, do not randomly sample
            if len(filtered_profiles) >= flights_per_request:
                filtered_profiles = filtered_profiles.sample(flights_per_request)

            # Make request for flight track points for each unique flight id in the filtered flight profiles results and obtain results
            # NOTE: By default, date_delta splits requests by hour
            track_points = trino.history(
                start=start,
                stop=stop,
                icao24=list(set(filtered_profiles['icao24'].unique().tolist()))
            )

            # Create partition columns for year, month, day, hour
            track_points['year'] = track_points['time'].dt.year
            track_points['month'] = track_points['time'].dt.month
            track_points['day'] = track_points['time'].dt.day
            track_points['hour'] = track_points['time'].dt.hour

            # Save to s3 with specific partition columns
            pbar.set_description(f'Saving Extraction {extract_num+1} of {num_iters}: {start} to {stop}', refresh=True)
            wr.s3.to_parquet(
                df=track_points,
                path=output_path,
                dataset=True,
                partition_cols=["year", "month", "day", "hour"],
                compression="snappy"  # Optional compression
            )

            # Save checkpoint
            save_checkpoint(
                session_state=dict(
                    output_path=output_path,
                    flights_per_request=flights_per_request,
                    hours_interval=hours_interval,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    current_datetime=current_datetime,
                    extract_num=extract_num,
                    num_iters=num_iters,
                    start=start,
                    stop=stop,
                ),
                path=os.path.join(DEFAULT_CHECKPOINT_DIR, SESSION_ID, 'track_points_session_state.json')
            )

            extract_num += 1
            current_datetime = start
            pbar.update(1)

def get_flight_profiles(trino: Trino, airports: set, **kwargs):
    print('[WARNING] Function to get flight profiles not yet implemented.')

def get_flight_messages(trino: Trino, airports: set, **kwargs):
    print('[WARNING] Function to get flight messages not yet implemented.')

def main():
    args = parser.parse_args()
    # print(json.dumps(args.__dict__, indent=2))

    # Load config for session
    config_path = DEFAULT_CONFIG if not os.path.exists('.env') else '.env'
    print(f'Loading from config file, "{config_path}"')
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Initialize trino database session
    trino = Trino()

    # Get airports and create unique lookup for only the US airports
    airports_df = pd.read_csv('../datasets/airports/airports.csv')
    airports = set(airports_df[airports_df['country'] == 'US']['icao'].unique().tolist())
    print(f'Unique airports: {len(airports)}')
    
    # Get flight track points data if enbaled in configuration
    if config['track_points']:
        print('Getting track points data...')
        get_track_points(trino, airports, **config['parameters'])

    # Get flight profiles data if enbaled in configuration
    if config['flight_profiles']:
        print('Getting flight profiles data...')
        get_flight_profiles(trino, airports, **config['parameters'])

    # Get flight messages data if enabled in configuration
    if config['flight_messages']:
        print('Getting flight messages data...')
        get_flight_messages(trino, airports, **config['parameters'])

if __name__ == '__main__':
    main()

