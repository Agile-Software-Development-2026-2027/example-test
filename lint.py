import re
import sys
from pathlib import Path

from check import normalize, read, require

USAGE = "usage: python3 lint.py <your output>"
NAME = r"[!-~]+"
COUNT = r"[1-9][0-9]*"
LINE = re.compile(
    rf"OK|none|0|{COUNT}"
    rf"|ERROR (invalid command|unknown pizza|not enough {NAME})"
    rf"|{NAME} {COUNT}( {NAME} {COUNT})*"
)


def first_error(output: str) -> str | None:
    for number, line in enumerate(normalize(output), start=1):
        if not line.isascii():
            return f"answer {number}: non-ASCII character"
        if not LINE.fullmatch(line):
            return f"answer {number}: unexpected format {line!r}"
    return None


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(USAGE)
    output = Path(sys.argv[1])
    require([output], USAGE)
    error = first_error(read(output))
    print("Y" if error is None else f"N {error}")
    sys.exit(0 if error is None else 1)


if __name__ == "__main__":
    main()
