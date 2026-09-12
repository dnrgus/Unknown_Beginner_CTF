import re
import sys
import zipfile
from pathlib import Path


def main():
    archive = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("challenges/misc/hidden-file/challenge/hidden-file.zip")
    with zipfile.ZipFile(archive) as zf:
        for name in zf.namelist():
            data = zf.read(name).decode(errors="ignore")
            flag = re.search(r"UNKNOWN\{[^}]+\}", data)
            if flag:
                print(flag.group(0))
                return
    raise SystemExit("flag not found")


if __name__ == "__main__":
    main()
