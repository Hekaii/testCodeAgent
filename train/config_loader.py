import json
import os


def load_experiment_config(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_dataset_paths(config, data_dir):
    dataset_config = config.get("dataset", {})
    resolved = {}
    for split in ("train", "dev", "test"):
        filename = dataset_config.get(split + "_file", split + ".csv")
        resolved[split] = os.path.join(data_dir, filename)
    return resolved


def ensure_file_exists(path):
    if not os.path.exists(path):
        raise IOError("Required file does not exist: {0}".format(path))
