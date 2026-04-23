from __future__ import annotations

import math

import numpy as np
import pandas as pd

from src.evaluation.metrics import top_k_metrics


def build_scored_ranking_table(
    features: pd.DataFrame,
    y_true,
    scores,
    share: float,
) -> pd.DataFrame:
    score_values = np.asarray(scores)
    y_values = np.asarray(y_true)
    target_count = max(1, math.ceil(len(score_values) * share))
    order = np.argsort(-score_values)

    selected = np.zeros(len(score_values), dtype=bool)
    selected[order[:target_count]] = True

    ranked = features.copy()
    ranked.insert(0, "row_id", ranked.index)
    ranked["actual_target"] = y_values
    ranked["model_score"] = score_values
    ranked["selected_for_outreach"] = selected
    ranked["priority_rank"] = ranked["model_score"].rank(method="first", ascending=False).astype(int)
    return ranked.sort_values(by="priority_rank").reset_index(drop=True)


def build_targeting_summary_table(model_name: str, y_true, scores, share: float) -> pd.DataFrame:
    metrics = top_k_metrics(y_true=y_true, scores=scores, share=share)
    return pd.DataFrame(
        [
            {
                "model": model_name,
                "targeting_rule": f"Select the top {int(share * 100)}% highest-scoring customers.",
                "target_share": share,
                "targeted_customers": metrics["targeted_customers"],
                "positives_captured": metrics["positives_captured"],
                "precision_at_share": metrics["precision_at_share"],
                "recall_at_share": metrics["recall_at_share"],
                "threshold_score": metrics["threshold_score"],
            }
        ]
    )
