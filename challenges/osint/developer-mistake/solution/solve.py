import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def main():
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("challenges/osint/developer-mistake/challenge/repo")
    if not (repo / ".git").exists():
        archive = repo.parent / "developer-mistake-repo.zip"
        if not archive.exists():
            raise SystemExit("repo or developer-mistake-repo.zip not found")
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(tmpdir)
            repo = Path(tmpdir) / "repo"
            log = subprocess.check_output(["git", "-C", str(repo), "log", "--all", "--patch"], text=True)
    else:
        log = subprocess.check_output(["git", "-C", str(repo), "log", "--all", "--patch"], text=True)
    flag = re.search(r"UNKNOWN\{[^}]+\}", log)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
