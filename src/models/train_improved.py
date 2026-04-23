from __future__ import annotations

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

from src.config import RANDOM_STATE
from src.features.build_features import build_preprocessor
from src.models.common import ModelBundle


def train_improved_model(features: pd.DataFrame, target: pd.Series) -> ModelBundle:
    preprocessor = build_preprocessor(features)
    transformed = preprocessor.fit_transform(features)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()

    estimator = GradientBoostingClassifier(random_state=RANDOM_STATE)
    estimator.fit(transformed, target)

    return ModelBundle(
        name="gradient_boosting",
        preprocessor=preprocessor,
        estimator=estimator,
        feature_names=list(preprocessor.get_feature_names_out()),
        requires_dense=True,
    )

