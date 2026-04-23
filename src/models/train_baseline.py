from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.features.build_features import build_preprocessor
from src.models.common import ModelBundle


def train_baseline_model(features: pd.DataFrame, target: pd.Series) -> ModelBundle:
    preprocessor = build_preprocessor(features)
    transformed = preprocessor.fit_transform(features)

    estimator = LogisticRegression(max_iter=1000)
    estimator.fit(transformed, target)

    return ModelBundle(
        name="logistic_regression",
        preprocessor=preprocessor,
        estimator=estimator,
        feature_names=list(preprocessor.get_feature_names_out()),
        requires_dense=False,
    )

