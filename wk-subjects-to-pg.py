import requests
from pathlib import Path
import psycopg
from psycopg.types.json import Jsonb
import json
from pprint import pprint

path_root = Path(__file__).parent.resolve()
path_api_key = path_root.joinpath('api-key.txt')


api_key = path_api_key.read_text()
session = requests.Session()
session.headers.update({'Authorization': f'Bearer {api_key}'})

one_assignment_for_now = session.get('https://api.wanikani.com/v2/subjects', params={'ids': '10'}).json()
pprint(one_assignment_for_now['data'][0])