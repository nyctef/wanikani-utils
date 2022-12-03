import sys
import webvtt
from python_utils import ensure_utf8_stdout

ensure_utf8_stdout()

if len(sys.argv) <= 1:
    print("Usage: [path/to/subtitles.vtt]")
    sys.exit(1)

path = sys.argv[1]

for caption in webvtt.read(path):
    # bug (?) in webvtt: not handling this xml escape for us
    text = caption.text.replace("&lrm;", "")
    print(text)
