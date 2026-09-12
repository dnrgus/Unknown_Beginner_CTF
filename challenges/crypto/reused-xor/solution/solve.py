import re
import sys
from pathlib import Path


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("challenges/crypto/reused-xor/challenge/ciphertext.hex")
    data = bytes.fromhex(path.read_text().strip())
    for key in range(256):
        candidate = bytes(byte ^ key for byte in data)
        text = candidate.decode(errors="ignore")
        flag = re.search(r"UNKNOWN\{[^}]+\}", text)
        if flag:
            print(flag.group(0))
            return
    raise SystemExit("flag not found")


if __name__ == "__main__":
    main()
