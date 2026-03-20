import argparse
import os

from train.config_loader import ensure_file_exists, load_experiment_config, resolve_dataset_paths
from train.dataset_reader import load_datasets
from train.reporting import ensure_parent, write_epoch_history_csv, write_final_metrics_csv, write_json
from train.trainer import run_training


DEFAULT_CONFIG = os.path.join("configs", "experiment.json")
DEFAULT_DATA_DIR = os.path.join("data", "raw")
DEFAULT_OUTPUT = os.path.join("outputs", "reports", "final_metrics.csv")
DEFAULT_LOG = os.path.join("logs", "train.log")


def build_parser():
    parser = argparse.ArgumentParser(description="Simulated paper training pipeline")
    parser.add_argument("--mode", choices=["dry-run", "baseline", "train"], default="train")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--log-path", default=DEFAULT_LOG)
    parser.add_argument("--epochs", type=int, default=0)
    return parser


def resolve_epochs(config, mode, explicit_epochs):
    if explicit_epochs and explicit_epochs > 0:
        return explicit_epochs

    training = config.get("training", {})
    if mode == "baseline":
        return int(training.get("baseline_epochs", 4))
    return int(training.get("train_epochs", 8))


def print_dry_run(config, dataset_paths, output_path, epochs):
    print("Dry run succeeded.")
    print("Project:", config.get("projectName", "unknown"))
    print("Resolved datasets:")
    for split in ("train", "dev", "test"):
        print("  - {0}: {1}".format(split, dataset_paths[split]))
    print("Resolved epochs:", epochs)
    print("Expected output:", output_path)


def main():
    args = build_parser().parse_args()
    ensure_file_exists(args.config)
    config = load_experiment_config(args.config)
    dataset_paths = resolve_dataset_paths(config, args.data_dir)
    for path in dataset_paths.values():
        ensure_file_exists(path)

    epochs = resolve_epochs(config, args.mode, args.epochs)
    if args.mode == "dry-run":
        print_dry_run(config, dataset_paths, args.output, epochs)
        return 0

    datasets = load_datasets(dataset_paths)
    ensure_parent(args.log_path)

    with open(args.log_path, "w", encoding="utf-8") as log_handle:
        history, final_metrics, dataset_summary = run_training(
            datasets=datasets,
            config=config,
            mode=args.mode,
            epochs=epochs,
            log_handle=log_handle,
        )

    write_final_metrics_csv(args.output, final_metrics)
    output_dir = os.path.dirname(args.output)
    write_epoch_history_csv(os.path.join(output_dir, "epoch_metrics.csv"), history)
    write_json(
        os.path.join(output_dir, "run_summary.json"),
        {
            "configPath": args.config,
            "dataDir": args.data_dir,
            "outputCsvPath": args.output,
            "logPath": args.log_path,
            "datasetSummary": dataset_summary,
            "finalMetrics": final_metrics,
        },
    )

    print(
        "Finished mode={0} epochs={1} score={2} output={3}".format(
            args.mode,
            final_metrics["epochs"],
            final_metrics["score"],
            args.output,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
