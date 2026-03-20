import csv
import json
import os


def ensure_parent(path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def write_final_metrics_csv(path, final_metrics):
    ensure_parent(path)
    fieldnames = [
        "mode",
        "epochs",
        "score",
        "macro_f1",
        "precision",
        "recall",
        "train_val_gap",
        "loss_std_last5",
        "best_epoch",
        "train_samples",
        "dev_samples",
        "test_samples",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(final_metrics)


def write_epoch_history_csv(path, history):
    ensure_parent(path)
    fieldnames = ["epoch", "loss", "score", "macro_f1", "train_score", "train_val_gap"]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in history:
            writer.writerow(row)


def write_json(path, payload):
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
