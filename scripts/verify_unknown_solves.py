import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def docker_path(path):
    return str(path).replace("\\", "/")


def command_for(name, command):
    return {"name": name, "command": command}


def main():
    docker_root = docker_path(ROOT)
    checks = [
        command_for(
            "WEB-01 Source Hunter",
            [
                PYTHON,
                "challenges/web/source-hunter/solution/solve.py",
                "http://localhost:8101",
            ],
        ),
        command_for(
            "WEB-02 Cookie Monster",
            [
                PYTHON,
                "challenges/web/cookie-monster/solution/solve.py",
                "http://localhost:8102",
            ],
        ),
        command_for(
            "WEB-03 Baby SQL",
            [
                PYTHON,
                "challenges/web/baby-sql/solution/solve.py",
                "http://localhost:8103",
            ],
        ),
        command_for(
            "PWN-01 Password Please",
            [
                PYTHON,
                "challenges/pwn/password-please/solution/solve.py",
                "localhost",
                "8201",
            ],
        ),
        command_for(
            "PWN-02 Overflow Me",
            [
                PYTHON,
                "challenges/pwn/overflow-me/solution/solve.py",
                "localhost",
                "8202",
            ],
        ),
        command_for(
            "PWN-03 Return to Win",
            [
                PYTHON,
                "challenges/pwn/return-to-win/solution/solve.py",
                "localhost",
                "8203",
            ],
        ),
        command_for(
            "REV-01 Find the Password",
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{docker_root}:/work",
                "-w",
                "/work",
                "python:3.12-bookworm",
                "python",
                "challenges/reversing/find-the-password/solution/solve.py",
            ],
        ),
        command_for(
            "REV-02 Simple Check",
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{docker_root}:/work",
                "-w",
                "/work",
                "python:3.12-bookworm",
                "python",
                "challenges/reversing/simple-check/solution/solve.py",
            ],
        ),
        command_for(
            "REV-03 XOR Password",
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{docker_root}:/work",
                "-w",
                "/work",
                "python:3.12-bookworm",
                "python",
                "challenges/reversing/xor-password/solution/solve.py",
            ],
        ),
        command_for(
            "CRYPTO-01 Caesar Salad",
            [PYTHON, "challenges/crypto/caesar-salad/solution/solve.py"],
        ),
        command_for(
            "CRYPTO-02 Base Adventure",
            [PYTHON, "challenges/crypto/base-adventure/solution/solve.py"],
        ),
        command_for(
            "CRYPTO-03 Reused XOR",
            [PYTHON, "challenges/crypto/reused-xor/solution/solve.py"],
        ),
        command_for(
            "OSINT-01 Hidden Username",
            [PYTHON, "challenges/osint/hidden-username/solution/solve.py"],
        ),
        command_for(
            "OSINT-02 Where Is This?",
            [PYTHON, "challenges/osint/where-is-this/solution/solve.py"],
        ),
        command_for(
            "OSINT-03 Developer Mistake",
            [PYTHON, "challenges/osint/developer-mistake/solution/solve.py"],
        ),
        command_for(
            "MISC-01 Hidden File",
            [PYTHON, "challenges/misc/hidden-file/solution/solve.py"],
        ),
        command_for(
            "MISC-02 Magic Bytes",
            [PYTHON, "challenges/misc/magic-bytes/solution/solve.py"],
        ),
        command_for(
            "MISC-03 Metadata", [PYTHON, "challenges/misc/metadata/solution/solve.py"]
        ),
    ]

    failures = []
    for check in checks:
        result = subprocess.run(
            check["command"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        output = result.stdout.strip()
        if result.returncode == 0 and output.startswith("UNKNOWN{"):
            print(f"[PASS] {check['name']} -> {output}")
        else:
            print(f"[FAIL] {check['name']}")
            if output:
                print(output)
            if result.stderr.strip():
                print(result.stderr.strip())
            failures.append(check["name"])

    if failures:
        raise SystemExit(f"{len(failures)} solve checks failed")

    print("[DONE] 18/18 solve checks passed")


if __name__ == "__main__":
    main()
