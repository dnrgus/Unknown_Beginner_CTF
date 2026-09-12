import re
import sys
from pathlib import Path


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("challenges/osint/hidden-username/challenge")
    profile = (base / "profile.html").read_text()
    username = re.search(r"canonical username:\s*([a-z0-9_]+)", profile).group(1)
    candidate = (base / "archive" / f"{username}.txt").read_text()
    flag = re.search(r"UNKNOWN\{[^}]+\}", candidate)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
