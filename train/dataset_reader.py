import csv


def load_split(path):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(row)
    return rows


def load_datasets(paths):
    return {split: load_split(path) for split, path in paths.items()}
