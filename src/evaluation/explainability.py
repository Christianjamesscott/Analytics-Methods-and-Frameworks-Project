from __future__ import annotations

import numpy as np
import pandas as pd

from src.models.common import ModelBundle


def _prettify_feature_name(feature_name: str) -> str:
    cleaned = feature_name.replace("numeric__", "").replace("categorical__", "")
    if "_" in cleaned:
        field, value = cleaned.split("_", 1)
        return f"{field.replace('.', ' ').replace('_', ' ')} = {value.replace('.', ' ').replace('_', ' ')}"
    return cleaned.replace(".", " ").replace("_", " ")


def baseline_coefficient_table(bundle: ModelBundle, top_n: int = 20) -> pd.DataFrame:
    coefficients = np.ravel(bundle.estimator.coef_)
    table = pd.DataFrame(
        {
            "feature": bundle.feature_names,
            "feature_label": [_prettify_feature_name(name) for name in bundle.feature_names],
            "coefficient": coefficients,
            "odds_ratio": np.exp(coefficients),
        }
    )
    return table.reindex(table["coefficient"].abs().sort_values(ascending=False).index).head(top_n)


def feature_importance_table(bundle: ModelBundle, top_n: int = 20) -> pd.DataFrame:
    if not hasattr(bundle.estimator, "feature_importances_"):
        raise ValueError(f"Model '{bundle.name}' does not expose feature importances.")

    table = pd.DataFrame(
        {
            "feature": bundle.feature_names,
            "feature_label": [_prettify_feature_name(name) for name in bundle.feature_names],
            "importance": bundle.estimator.feature_importances_,
        }
    )
    return table.sort_values(by="importance", ascending=False).head(top_n)


def build_driver_summary_table(
    baseline_table: pd.DataFrame,
    improved_table: pd.DataFrame,
) -> pd.DataFrame:
    positive_baseline = baseline_table.sort_values(by="coefficient", ascending=False).head(2)
    negative_baseline = baseline_table.sort_values(by="coefficient", ascending=True).head(1)

    rows: list[dict[str, object]] = []
    for rank, (_, row) in enumerate(positive_baseline.iterrows(), start=1):
        rows.append(
            {
                "model": "logistic_regression",
                "insight_rank": rank,
                "insight": (
                    f"Higher values or presence of '{row['feature_label']}' are associated with a higher outreach priority "
                    f"in the baseline model."
                ),
            }
        )

    for _, row in negative_baseline.iterrows():
        rows.append(
            {
                "model": "logistic_regression",
                "insight_rank": len(rows) + 1,
                "insight": (
                    f"'{row['feature_label']}' is associated with a lower predicted outreach priority in the baseline model."
                ),
            }
        )

    for rank, (_, row) in enumerate(improved_table.head(3).iterrows(), start=1):
        rows.append(
            {
                "model": "gradient_boosting",
                "insight_rank": rank,
                "insight": (
                    f"'{row['feature_label']}' is among the most influential inputs in the improved model's ranking logic."
                ),
            }
        )

    return pd.DataFrame(rows)
