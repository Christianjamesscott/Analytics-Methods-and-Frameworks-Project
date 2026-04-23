from __future__ import annotations

import numpy as np
import pandas as pd

from src.evaluation.metrics import selected_mask


def _age_bucket(series: pd.Series) -> pd.Series:
    return pd.cut(
        series,
        bins=[17, 29, 39, 49, 59, 120],
        labels=["18-29", "30-39", "40-49", "50-59", "60+"],
    )


def build_segment_sanity_table(
    features: pd.DataFrame,
    y_true,
    scores,
    share: float,
    segment_column: str = "age",
) -> pd.DataFrame:
    if segment_column not in features.columns:
        raise ValueError(f"Segment column '{segment_column}' not found in feature frame.")

    selected, _ = selected_mask(scores=scores, share=share)

    if segment_column == "age":
        segments = _age_bucket(features[segment_column])
        segment_name = "age_bucket"
    else:
        segments = features[segment_column].astype(str)
        segment_name = segment_column

    frame = pd.DataFrame(
        {
            "segment": segments.astype(str),
            "actual_target": np.asarray(y_true),
            "selected_for_outreach": selected,
        }
    )
    frame["selected_positive"] = frame["actual_target"] * frame["selected_for_outreach"].astype(int)

    summary = (
        frame.groupby("segment", dropna=False)
        .agg(
            customers=("segment", "size"),
            positives=("actual_target", "sum"),
            selected_customers=("selected_for_outreach", "sum"),
            selected_positives=("selected_positive", "sum"),
        )
        .reset_index()
    )
    summary["segment_variable"] = segment_name
    summary["positive_rate"] = summary["positives"] / summary["customers"]
    summary["selection_rate"] = summary["selected_customers"] / summary["customers"]
    summary["selected_precision"] = summary["selected_positives"] / summary["selected_customers"].where(
        summary["selected_customers"] > 0, np.nan
    )
    ordered_columns = [
        "segment_variable",
        "segment",
        "customers",
        "positives",
        "positive_rate",
        "selected_customers",
        "selected_positives",
        "selection_rate",
        "selected_precision",
    ]
    return summary[ordered_columns].sort_values(by="segment")
