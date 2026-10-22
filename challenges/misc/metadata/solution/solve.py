import re
import sys
from pathlib import Path

from PIL import Image


def main():
    path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("challenges/misc/metadata/challenge/ordinary.png")
    )
    with Image.open(path) as img:
        text = "\n".join(str(value) for value in img.info.values())
    flag = re.search(r"UNKNOWN\{[^}]+\}", text)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
