from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import (
    DATASET_PATHS,
    DEFAULT_DATASET_NAME,
    POSITIVE_TARGET_VALUE,
    PROACTIVE_EXCLUDED_COLUMNS,
    TARGET_COLUMN,
)


def list_available_datasets() -> list[str]:
    return sorted(DATASET_PATHS.keys())


def resolve_dataset_path(dataset_name: str = DEFAULT_DATASET_NAME) -> Path:
    try:
        path = DATASET_PATHS[dataset_name]
    except KeyError as exc:
        available = ", ".join(list_available_datasets())
        raise ValueError(f"Unknown dataset '{dataset_name}'. Available: {available}") from exc

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return path


def load_dataset(dataset_name: str = DEFAULT_DATASET_NAME) -> pd.DataFrame:
    path = resolve_dataset_path(dataset_name)
    return pd.read_csv(path, sep=";")


def build_modeling_frame(frame: pd.DataFrame) -> pd.DataFrame:
    present_exclusions = [column for column in PROACTIVE_EXCLUDED_COLUMNS if column in frame.columns]
    return frame.drop(columns=present_exclusions).copy()


def split_features_target(
    frame: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
) -> tuple[pd.DataFrame, pd.Series]:
    features = frame.drop(columns=[target_column]).copy()
    target = frame[target_column].eq(POSITIVE_TARGET_VALUE).astype(int)
    target.name = target_column
    return features, target
