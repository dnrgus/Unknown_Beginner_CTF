import re
import subprocess
import sys


def main():
    binary = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "challenges/reversing/xor-password/challenge/xor-password"
    )
    encoded_password = [22, 53, 40, 5, 50, 47, 52, 46, 63, 40]
    password = bytes(value ^ 0x5A for value in encoded_password)
    result = subprocess.run(
        [binary],
        input=password + b"\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    text = result.stdout.decode(errors="replace")
    flag = re.search(r"UNKNOWN\{[^}]+\}", text)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
