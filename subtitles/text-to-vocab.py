import nagisa
from pathlib import Path
from pprint import pprint
from collections import defaultdict
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

if len(sys.argv) <= 1:
    print("Usage: [path/to/file.txt]")
    sys.exit(1)

path = sys.argv[1]

text = Path(path).read_text(encoding='utf-8')

# run nagisa against the file
result = nagisa.tagging(text)
# "pos" = "part of speech"
l = zip(result.postags, result.words)

# use `set` here to dedupe words
grouped = defaultdict(set)
for pos, word in l:
    # using re.sub to strip out all whitespace
    grouped[pos].add(re.sub(r"\s+", "", word))

for pos, words in grouped.items():
    print(pos)
    for word in words:
        print(f"  {word}")