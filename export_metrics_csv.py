import csv
import json


def main():
    with open("outputs/latest/metrics.json", "r", encoding="utf-8") as metrics_file:
        metrics = json.load(metrics_file)

    with open("output/result.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["指标", "指标值"])
        for key, value in metrics.items():
            writer.writerow([key, value])


if __name__ == "__main__":
    main()
