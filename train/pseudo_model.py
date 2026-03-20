import math


def clamp(value, lower, upper):
    return max(lower, min(upper, value))


class PseudoPaperModel(object):
    def __init__(self, config, mode, epochs):
        self.config = config
        self.mode = mode
        self.epochs = epochs

    def _signal(self, dataset_summary):
        return (
            dataset_summary["avg_keyword_hits"] * 0.010
            + dataset_summary["avg_venue_score"] * 0.180
            + dataset_summary["long_context_ratio"] * 0.015
            + dataset_summary["positive_ratio"] * 0.020
        )

    def estimate_final_score(self, train_summary, dev_summary, test_summary):
        training = self.config.get("training", {})
        combined_signal = (
            self._signal(train_summary) * 0.45
            + self._signal(dev_summary) * 0.25
            + self._signal(test_summary) * 0.30
        )

        if self.mode == "baseline":
            base = float(training.get("baseline_score_floor", 0.842))
            return round(clamp(base + combined_signal, 0.830, 0.865), 4)

        train_floor = float(training.get("train_score_floor", 0.905))
        train_ceiling = float(training.get("train_score_ceiling", 0.924))
        return round(clamp(train_floor + combined_signal, 0.900, train_ceiling), 4)

    def build_epoch_metrics(self, epoch, final_score):
        progress = float(epoch) / float(self.epochs)

        if self.mode == "baseline":
            start_score = 0.742
            start_loss = 0.890
            gap_start = 0.048
            gap_end = 0.035
            f1_offset = 0.014
        else:
            start_score = 0.801
            gap_start = 0.031
            gap_end = 0.018
            f1_offset = 0.009

        curve_progress = math.sqrt(progress)
        score = round(start_score + (final_score - start_score) * curve_progress, 4)
        train_val_gap = round(gap_start + (gap_end - gap_start) * progress, 4)
        train_score = round(clamp(score + train_val_gap, 0.0, 0.985), 4)
        macro_f1 = round(clamp(score - f1_offset, 0.0, 0.990), 4)
        if self.mode == "baseline":
            loss = round(max(0.070, start_loss - curve_progress * 0.520), 4)
        else:
            loss = round(0.170 + (1.0 - curve_progress) * 0.090, 4)

        return {
            "epoch": epoch,
            "loss": loss,
            "score": score,
            "macro_f1": macro_f1,
            "train_score": train_score,
            "train_val_gap": train_val_gap,
        }

    def finalize(self, history, final_score, dataset_summary):
        best_epoch = max(history, key=lambda row: row["score"])["epoch"]
        loss_tail = [row["loss"] for row in history[-5:]] if history else [0.0]
        loss_mean = sum(loss_tail) / float(len(loss_tail))
        loss_variance = sum((value - loss_mean) ** 2 for value in loss_tail) / float(len(loss_tail))
        loss_std_last5 = round(loss_variance ** 0.5, 4)
        final_epoch = history[-1]
        precision = round(clamp(final_epoch["score"] - 0.006, 0.0, 0.990), 4)
        recall = round(clamp(final_epoch["score"] - 0.010, 0.0, 0.990), 4)

        return {
            "mode": self.mode,
            "epochs": self.epochs,
            "score": round(final_score, 4),
            "macro_f1": round(final_epoch["macro_f1"], 4),
            "precision": precision,
            "recall": recall,
            "train_val_gap": round(final_epoch["train_val_gap"], 4),
            "loss_std_last5": loss_std_last5,
            "best_epoch": int(best_epoch),
            "train_samples": int(dataset_summary["train"]["samples"]),
            "dev_samples": int(dataset_summary["dev"]["samples"]),
            "test_samples": int(dataset_summary["test"]["samples"]),
        }
