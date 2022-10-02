import gzip
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint
sys.stdout.reconfigure(encoding='utf-8')


if len(sys.argv) <= 1:
    print("Usage: [path/to/kanjidic2.xml.gz]")
    sys.exit(1)

skip_to_char = defaultdict(list)
char_to_skip = {}

with gzip.open(sys.argv[1]) as fin:
    tree = ET.parse(fin).getroot()
    for charElement in tree.findall('character'):
        char = charElement.find('literal').text
        skip = charElement.find(".//q_code[@qc_type='skip']").text
        char_to_skip[char] = skip
        skip_to_char[skip].append(char)

for entry in sorted(skip_to_char.items(), key=lambda x: len(x[1])):
    print(entry[0] + ": " + str(entry[1]))