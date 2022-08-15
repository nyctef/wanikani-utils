import requests
from pathlib import Path
import psycopg
from psycopg.types.json import Jsonb
import json
from pprint import pprint

path_root = Path(__file__).parent.resolve()
path_api_key = path_root.joinpath('api-key.txt')
path_db_str = path_root.joinpath('db-str.txt')


api_key = path_api_key.read_text()
session = requests.Session()
session.headers.update({'Authorization': f'Bearer {api_key}'})

url = 'https://api.wanikani.com/v2/subjects'
pprint(session.get(url, params={'hidden':'true'}).json())