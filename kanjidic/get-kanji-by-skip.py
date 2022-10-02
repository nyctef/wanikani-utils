import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import psycopg

if len(sys.argv) <= 1:
    print("Usage: [skip code 1-2-3]")
    sys.exit(1)

skip = sys.argv[1]

path_root = Path(__file__).parent.parent.resolve()
path_db_str = path_root.joinpath('db-str.txt')
db_str = path_db_str.read_text()
with psycopg.connect(db_str) as conn:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT radical, kanji FROM kanji_by_skip_radicals
            WHERE skip = %s""", (skip,)
        )
        for result in cur.fetchall():
            print(f"{result[0]}: {' '.join(result[1])}")