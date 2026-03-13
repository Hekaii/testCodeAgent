#!/usr/bin/env bash
set -euo pipefail

mkdir -p output
python train.py --mode train --epochs 5 --output outputs/latest/metrics.json
python export_metrics_csv.py
