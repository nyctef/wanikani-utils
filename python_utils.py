import io
import sys


def ensure_utf8_stdout():
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.version_info < (3, 7):
        raise Exception("Need to make stdout utf8")
    sys.stdout.reconfigure(encoding="utf-8")
