import re
import sys
from pathlib import Path


def main():
    path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("challenges/misc/magic-bytes/challenge/not_a_text.txt")
    )
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("not a png")
    flag = re.search(rb"UNKNOWN\{[^}]+\}", data)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0).decode())


if __name__ == "__main__":
    main()
