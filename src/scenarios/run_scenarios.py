from __future__ import annotations

import pandas as pd

from src.evaluation.metrics import top_k_metrics


def run_capacity_scenarios(
    y_true,
    scores,
    capacities: tuple[float, ...] = (0.10, 0.20, 0.30),
) -> pd.DataFrame:
    rows = []
    for capacity in capacities:
        metrics = top_k_metrics(y_true=y_true, scores=scores, share=capacity)
        metrics["scenario"] = f"top_{int(capacity * 100)}pct"
        rows.append(metrics)

    ordered_columns = [
        "scenario",
        "target_share",
        "targeted_customers",
        "positives_captured",
        "precision_at_share",
        "recall_at_share",
        "false_positives",
        "false_negatives",
        "threshold_score",
    ]
    return pd.DataFrame(rows)[ordered_columns]

