import csv
import sys
from pathlib import Path


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("challenges/osint/where-is-this/challenge")
    with (base / "mini-map-index.csv").open(newline="") as fp:
        for row in csv.DictReader(fp):
            if row["nearby_clue"] == "UNKNOWN Tower":
                print(row["flag"])
                return
    raise SystemExit("flag not found")


if __name__ == "__main__":
    main()
