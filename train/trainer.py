from train.feature_pipeline import build_split_features, summarize_split
from train.pseudo_model import PseudoPaperModel


def run_training(datasets, config, mode, epochs, log_handle):
    dataset_summary = {}
    for split, rows in datasets.items():
        feature_rows = build_split_features(rows, config)
        dataset_summary[split] = summarize_split(feature_rows)

    model = PseudoPaperModel(config, mode, epochs)
    final_score = model.estimate_final_score(
        dataset_summary["train"],
        dataset_summary["dev"],
        dataset_summary["test"],
    )

    history = []
    log_handle.write(
        "mode={0} epochs={1} train_samples={2} dev_samples={3} test_samples={4}\n".format(
            mode,
            epochs,
            dataset_summary["train"]["samples"],
            dataset_summary["dev"]["samples"],
            dataset_summary["test"]["samples"],
        )
    )

    for epoch in range(1, epochs + 1):
        metrics = model.build_epoch_metrics(epoch, final_score)
        history.append(metrics)
        log_handle.write(
            "epoch={epoch} loss={loss:.4f} score={score:.4f} macro_f1={macro_f1:.4f} "
            "train_score={train_score:.4f} train_val_gap={train_val_gap:.4f}\n".format(**metrics)
        )
        log_handle.flush()

    final_metrics = model.finalize(history, final_score, dataset_summary)
    return history, final_metrics, dataset_summary
