from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import (
    FEATURE_EXCLUSION_NOTES,
    MODEL_SELECTION_RULE,
    POSITIVE_TARGET_VALUE,
    PROACTIVE_EXCLUDED_COLUMNS,
    TARGET_COLUMN,
    TARGET_DEFINITION_NOTE,
)


def build_dataset_summary(
    frame: pd.DataFrame,
    dataset_name: str,
    dataset_path: Path,
    modeling_frame: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "dataset_name": dataset_name,
                "source_path": str(dataset_path),
                "rows": len(frame),
                "raw_columns": frame.shape[1],
                "modeling_columns": modeling_frame.shape[1],
                "excluded_columns_count": len(PROACTIVE_EXCLUDED_COLUMNS),
                "duplicate_rows": int(frame.duplicated().sum()),
                "missing_cells": int(frame.isna().sum().sum()),
                "target_positive_rate": round(float(frame[TARGET_COLUMN].eq(POSITIVE_TARGET_VALUE).mean()), 6),
            }
        ]
    )


def build_target_balance_table(
    frame: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
) -> pd.DataFrame:
    counts = frame[target_column].value_counts(dropna=False).rename_axis("target_value").reset_index(name="count")
    counts["share"] = counts["count"] / counts["count"].sum()
    return counts


def build_profile_summary(
    frame: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
) -> pd.DataFrame:
    target_rate = frame[target_column].eq(POSITIVE_TARGET_VALUE).mean()
    summary = [
        ("rows", len(frame)),
        ("columns", frame.shape[1]),
        ("duplicate_rows", int(frame.duplicated().sum())),
        ("missing_cells", int(frame.isna().sum().sum())),
        ("target_positive_rate", round(float(target_rate), 6)),
    ]
    return pd.DataFrame(summary, columns=["metric", "value"])


def build_data_dictionary(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for column in frame.columns:
        series = frame[column]
        sample_values = series.dropna().astype(str).unique()[:3]
        rows.append(
            {
                "column": column,
                "dtype": str(series.dtype),
                "non_null_count": int(series.notna().sum()),
                "missing_count": int(series.isna().sum()),
                "missing_pct": round(float(series.isna().mean()), 6),
                "unique_count": int(series.nunique(dropna=True)),
                "sample_values": " | ".join(sample_values),
            }
        )
    return pd.DataFrame(rows)


def build_target_definition_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "target_column": TARGET_COLUMN,
                "positive_class": POSITIVE_TARGET_VALUE,
                "business_definition": TARGET_DEFINITION_NOTE,
            }
        ]
    )


def build_cleaning_decisions_table(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = [
        {
            "decision_type": "data_quality",
            "field": "missing_values",
            "action": "retain_as_is",
            "reason": f"The dataset contains {int(frame.isna().sum().sum())} missing cells.",
        },
        {
            "decision_type": "data_quality",
            "field": "duplicate_rows",
            "action": "retain_as_is",
            "reason": f"The dataset contains {int(frame.duplicated().sum())} duplicate rows.",
        },
        {
            "decision_type": "model_selection",
            "field": "selection_rule",
            "action": "rank_by_precision_then_recall",
            "reason": MODEL_SELECTION_RULE,
        },
    ]

    for column in PROACTIVE_EXCLUDED_COLUMNS:
        if column in frame.columns:
            rows.append(
                {
                    "decision_type": "feature_scope",
                    "field": column,
                    "action": "exclude_from_modeling",
                    "reason": FEATURE_EXCLUSION_NOTES[column],
                }
            )

    return pd.DataFrame(rows)


def build_split_summary(
    x_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "train_rows": len(x_train),
                "test_rows": len(x_test),
                "train_positive_rate": round(float(y_train.mean()), 6),
                "test_positive_rate": round(float(y_test.mean()), 6),
                "train_features": x_train.shape[1],
                "split_strategy": "stratified_random_split",
            }
        ]
    )
