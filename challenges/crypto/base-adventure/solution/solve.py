import base64
import binascii
import re
import sys
from pathlib import Path


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("challenges/crypto/base-adventure/challenge/encoded.txt")
    data = path.read_text().strip().encode()
    step1 = base64.b64decode(data)
    step2 = binascii.unhexlify(step1)
    step3 = base64.b64decode(step2).decode()
    flag = re.search(r"UNKNOWN\{[^}]+\}", step3)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
