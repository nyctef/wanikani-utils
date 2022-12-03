from pathlib import Path
from collections import defaultdict
from pprint import pprint
from multiprocessing import Pool
import sys
import csv

import nagisa

from python_utils import ensure_utf8_stdout

ensure_utf8_stdout()


def run_nagisa(text: str):
    result = nagisa.tagging(text)
    # "pos" = "part of speech"
    # pprint(result.postags)
    return zip(result.postags, result.words)


def main():
    if len(sys.argv) <= 1:
        print("Usage: [path/to/file.txt]")
        sys.exit(1)

    path = sys.argv[1]

    lines = Path(path).read_text(encoding="utf-8").splitlines()
    # lines = lines[0:1000]
    table = csv.reader(lines, delimiter="\t")
    jps = [x[1] for x in table]

    with Pool() as multiprocessor_pool:
        parsed = multiprocessor_pool.map(run_nagisa, jps)

    result_by_count = defaultdict(int)
    for parsed_line in parsed:
        for (pos, word) in parsed_line:
            result_by_count[word] += 1

    sorted_result = [
        (k, v)
        for k, v in sorted(
            result_by_count.items(), key=lambda kvp: kvp[1], reverse=True
        )
    ]

    pprint(sorted_result)


if __name__ == "__main__":
    main()
