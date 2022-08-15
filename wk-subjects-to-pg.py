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
with psycopg.connect(db_str) as conn:
    with conn.cursor() as cur:
        url = 'https://api.wanikani.com/v2/subjects'
        while url is not None:
            print(url)
            page = session.get(url).json()
            for item in page['data']:
                id = item['id']
                data = item['data']

                print('.', end='')
                cur.execute("""INSERT INTO subjects (id, subject_data) VALUES (%s, %s);""", (id, Jsonb(data)))

            print()
            url = page['pages']['next_url']