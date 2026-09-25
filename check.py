import sys
from itertools import zip_longest
from pathlib import Path

USAGE = "usage: python3 check.py <your output> <official output>"


def require(paths: list[Path], usage: str) -> None:
    missing = [path for path in paths if not path.is_file()]
    if missing:
        sys.exit(f"{missing[0]} not found\n{usage}")


def normalize(text: str) -> list[str]:
    return [" ".join(line.split()) for line in text.splitlines() if line.strip()]


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="replace")


def first_mismatch(expected: list[str], got: list[str]) -> str | None:
    pairs = zip_longest(expected, got, fillvalue="")
    for number, (want, have) in enumerate(pairs, start=1):
        if want != have:
            wanted = repr(want) if want else "nothing"
            shown = repr(have) if have else "no output"
            return f"answer {number}: expected {wanted}, got {shown}"
    return None


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(USAGE)
    mine, official = Path(sys.argv[1]), Path(sys.argv[2])
    require([mine, official], USAGE)
    problem = first_mismatch(normalize(read(official)), normalize(read(mine)))
    print("PASS" if problem is None else f"FAIL {problem}")
    sys.exit(0 if problem is None else 1)


if __name__ == "__main__":
    main()
