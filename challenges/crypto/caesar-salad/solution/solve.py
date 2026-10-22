import re
import sys
from pathlib import Path


def rot13(text):
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + 13) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + 13) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


def main():
    path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("challenges/crypto/caesar-salad/challenge/message.txt")
    )
    decoded = rot13(path.read_text())
    flag = re.search(r"UNKNOWN\{[^}]+\}", decoded)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
