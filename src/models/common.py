from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer


@dataclass
class ModelBundle:
    name: str
    preprocessor: ColumnTransformer
    estimator: Any
    feature_names: list[str]
    requires_dense: bool = False


def transform_features(bundle: ModelBundle, features: pd.DataFrame):
    transformed = bundle.preprocessor.transform(features)
    if bundle.requires_dense and hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    return transformed


def score_rows(bundle: ModelBundle, features: pd.DataFrame) -> np.ndarray:
    transformed = transform_features(bundle, features)
    if hasattr(bundle.estimator, "predict_proba"):
        return bundle.estimator.predict_proba(transformed)[:, 1]
    return bundle.estimator.decision_function(transformed)

