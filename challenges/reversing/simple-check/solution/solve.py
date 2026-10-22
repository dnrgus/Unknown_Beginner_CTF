import re
import subprocess
import sys


def main():
    binary = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "challenges/reversing/simple-check/challenge/simple-check"
    )
    result = subprocess.run(
        [binary],
        input=b"rev_check7\n",
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
