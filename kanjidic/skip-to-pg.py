import gzip
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import psycopg

if len(sys.argv) <= 1:
    print("Usage: [path/to/kanjidic2.xml.gz]")
    sys.exit(1)

path_root = Path(__file__).parent.parent.resolve()
path_db_str = path_root.joinpath('db-str.txt')

skip_rad_to_char = defaultdict(list)

with gzip.open(sys.argv[1]) as fin:
    tree = ET.parse(fin).getroot()
    for charElement in tree.findall('character'):
        char = charElement.find('literal').text
        skip = charElement.find(".//q_code[@qc_type='skip']").text
        radicalNum = charElement.find(".//rad_value[@rad_type='classical']").text
        # 0x2F00 is the start of the radical block in unicode: https://en.wikipedia.org/wiki/Kangxi_Radicals_(Unicode_block)
        # subtract 1 since the radical number is 1-indexed but the unicode block is 0-indexed
        radical = chr(0x2F00 - 1 + int(radicalNum))
        skip_rad_to_char[(skip, radical)].append(char)

db_str = path_db_str.read_text()
with psycopg.connect(db_str) as conn:
    with conn.cursor() as cur:
        for key, value in sorted(skip_rad_to_char.items(), key=lambda x: len(x[1])):
            skip = key[0]
            radical = key[1]
            kanji = value
            cur.execute(
                """INSERT INTO kanji_by_skip_radicals (skip, radical, kanji) VALUES (%s, %s, %s)""",
                (skip, radical, kanji))