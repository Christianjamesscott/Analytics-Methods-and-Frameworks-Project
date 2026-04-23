from __future__ import annotations

import math

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score


def _top_k_count(size: int, share: float) -> int:
    return max(1, math.ceil(size * share))


def selected_mask(scores, share: float) -> tuple[np.ndarray, float]:
    score_values = np.asarray(scores)
    count = _top_k_count(len(score_values), share)
    order = np.argsort(-score_values)
    selected = np.zeros(len(score_values), dtype=bool)
    selected[order[:count]] = True
    threshold = float(score_values[order[count - 1]])
    return selected, threshold


def top_k_metrics(y_true, scores, share: float) -> dict[str, float]:
    y_true_values = np.asarray(y_true)
    selected, threshold = selected_mask(scores, share)

    true_positive = int(((selected == 1) & (y_true_values == 1)).sum())
    false_positive = int(((selected == 1) & (y_true_values == 0)).sum())
    false_negative = int(((selected == 0) & (y_true_values == 1)).sum())
    true_negative = int(((selected == 0) & (y_true_values == 0)).sum())

    precision = true_positive / max(true_positive + false_positive, 1)
    recall = true_positive / max(true_positive + false_negative, 1)

    return {
        "target_share": share,
        "targeted_customers": int(selected.sum()),
        "threshold_score": threshold,
        "positives_captured": true_positive,
        "precision_at_share": precision,
        "recall_at_share": recall,
        "true_positives": true_positive,
        "false_positives": false_positive,
        "false_negatives": false_negative,
        "true_negatives": true_negative,
    }


def summarize_model_metrics(name: str, y_true, scores, share: float) -> dict[str, float]:
    metrics = top_k_metrics(y_true=y_true, scores=scores, share=share)
    metrics.update(
        {
            "model": name,
            "pr_auc": float(average_precision_score(y_true, scores)),
            "roc_auc": float(roc_auc_score(y_true, scores)),
        }
    )
    return metrics


def build_model_results_table(name: str, y_true, scores, share: float) -> pd.DataFrame:
    ordered_columns = [
        "model",
        "pr_auc",
        "roc_auc",
        "target_share",
        "targeted_customers",
        "positives_captured",
        "precision_at_share",
        "recall_at_share",
        "true_positives",
        "false_positives",
        "false_negatives",
        "true_negatives",
        "threshold_score",
    ]
    return pd.DataFrame([summarize_model_metrics(name=name, y_true=y_true, scores=scores, share=share)])[
        ordered_columns
    ]


def build_comparison_table(results: dict[str, np.ndarray], y_true, share: float) -> pd.DataFrame:
    rows = [
        summarize_model_metrics(name=model_name, y_true=y_true, scores=scores, share=share)
        for model_name, scores in results.items()
    ]
    ordered_columns = [
        "model",
        "pr_auc",
        "roc_auc",
        "target_share",
        "targeted_customers",
        "positives_captured",
        "precision_at_share",
        "recall_at_share",
        "false_positives",
        "false_negatives",
        "threshold_score",
    ]
    return pd.DataFrame(rows)[ordered_columns].sort_values(
        by=["precision_at_share", "recall_at_share", "pr_auc"],
        ascending=False,
    )


def build_tradeoff_table(model_name: str, y_true, scores, share: float) -> pd.DataFrame:
    metrics = top_k_metrics(y_true=y_true, scores=scores, share=share)
    rows = [
        {
            "model": model_name,
            "outcome_type": "true_positive",
            "count": metrics["true_positives"],
            "business_interpretation": "Strong-priority customers selected for proactive outreach.",
        },
        {
            "model": model_name,
            "outcome_type": "false_positive",
            "count": metrics["false_positives"],
            "business_interpretation": "Outreach effort spent on weaker-priority customers.",
        },
        {
            "model": model_name,
            "outcome_type": "false_negative",
            "count": metrics["false_negatives"],
            "business_interpretation": "Missed opportunity to prioritize a stronger candidate for outreach.",
        },
        {
            "model": model_name,
            "outcome_type": "true_negative",
            "count": metrics["true_negatives"],
            "business_interpretation": "Lower-priority customers left outside the top-20% queue.",
        },
    ]
    return pd.DataFrame(rows)


def build_decision_summary_table(model_name: str, y_true, scores, share: float) -> pd.DataFrame:
    metrics = top_k_metrics(y_true=y_true, scores=scores, share=share)
    rows = [
        {
            "decision_item": "recommended_model",
            "value": model_name,
        },
        {
            "decision_item": "targeting_rule",
            "value": f"Rank customers by model score and target the top {int(share * 100)}%.",
        },
        {
            "decision_item": "targeted_customers",
            "value": str(metrics["targeted_customers"]),
        },
        {
            "decision_item": "precision_at_target_share",
            "value": f"{metrics['precision_at_share']:.4f}",
        },
        {
            "decision_item": "recall_at_target_share",
            "value": f"{metrics['recall_at_share']:.4f}",
        },
        {
            "decision_item": "positives_captured",
            "value": str(metrics["positives_captured"]),
        },
    ]
    return pd.DataFrame(rows)
