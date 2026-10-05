from pathlib import Path


def load():
    rows = []
    for line in (Path(__file__).parent.parent / "patterns.txt").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            name, rx = line.split("\t", 1)
            rows.append((name, rx))
    return rows
