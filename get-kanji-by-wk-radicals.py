import sys
from pathlib import Path
import psycopg
from psycopg.types.json import Jsonb
import json
from pprint import pprint

path_root = Path(__file__).parent.resolve()
path_db_str = path_root.joinpath('db-str.txt')
db_str = path_db_str.read_text()

if len(sys.argv) <= 1:
    print("Usage: [radical-name-1] [radical-name-2] ...")
    sys.exit(1)

radical_names = sys.argv[1:]

with psycopg.connect(db_str) as conn:
    with conn.cursor() as cur:
        cur.execute("""select characters,components from kanji_by_wk_radicals where %s <@ components""", (radical_names,))
        for row in cur:
            print(f'{row[0]}: {", ".join(row[1])}')