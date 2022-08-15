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

db_str = path_db_str.read_text()

one_assignment_for_now = session.get('https://api.wanikani.com/v2/subjects', params={'ids': '10'}).json()
id = one_assignment_for_now['data'][0]['id']
data = one_assignment_for_now['data'][0]['data']

with psycopg.connect(db_str) as conn:
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO subjects (id, subject_data) VALUES (%s, %s);""", (id, Jsonb(data)))