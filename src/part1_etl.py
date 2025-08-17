'''
PART 1: ETL the dataset and save in `data/`

Here is the imbd_movie data:
https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true

It is in JSON format, so you'll need to handle accordingly and also figure out what's the best format for the two analysis parts. 
'''

import os
import pandas as pd
import json
import requests

# Create '/data' directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_dir, exist_ok=True)

# Load datasets and save to '/data'
def etl(): url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
response = requests.get(url)

    if response.status_code == 200:
        movies = json.loads(response.text)

        df = pd.json_normalize(movies) output_path = os.path.join(data_dir, 'imdb_movies.json')
        df.to_json(output_path, orient='records', lines=True)

        print("ETL complete. Saved to:", output_path)
    else:
        print("Failed to download data. Status code:", response.status_code)
