from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_recall_curve


def _finalize_plot(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_target_distribution(target_balance: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(6, 4))
    plt.bar(target_balance["target_value"], target_balance["count"], color=["#5B8FF9", "#5AD8A6"])
    plt.title("Target Distribution")
    plt.xlabel("Target")
    plt.ylabel("Customer Count")
    _finalize_plot(output_path)


def plot_model_comparison(model_comparison: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(8, 4.5))
    positions = range(len(model_comparison))
    width = 0.35
    plt.bar(
        [position - width / 2 for position in positions],
        model_comparison["precision_at_share"],
        width=width,
        label="Precision @ 20%",
        color="#5B8FF9",
    )
    plt.bar(
        [position + width / 2 for position in positions],
        model_comparison["recall_at_share"],
        width=width,
        label="Recall @ 20%",
        color="#5AD8A6",
    )
    plt.xticks(list(positions), model_comparison["model"])
    plt.ylim(0, 1)
    plt.ylabel("Metric Value")
    plt.title("Top-20% Decision Metrics by Model")
    plt.legend()
    _finalize_plot(output_path)


def plot_precision_recall_curve_for_model(model_name: str, y_true, scores, output_path: Path) -> None:
    precision, recall, _ = precision_recall_curve(y_true, scores)
    plt.figure(figsize=(6, 4.5))
    plt.plot(recall, precision, color="#5B8FF9", linewidth=2)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"Precision-Recall Curve: {model_name}")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    _finalize_plot(output_path)


def plot_feature_importance(importance_table: pd.DataFrame, output_path: Path, title: str) -> None:
    value_column = importance_table.columns[-1]
    table = importance_table.head(10).sort_values(by=value_column, ascending=True)
    plt.figure(figsize=(8, 5.5))
    plt.barh(table["feature_label"], table[value_column], color="#5B8FF9")
    plt.xlabel(value_column.replace("_", " ").title())
    plt.title(title)
    _finalize_plot(output_path)


def plot_scenario_comparison(scenario_table: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(7, 4.5))
    share_pct = scenario_table["target_share"] * 100
    plt.plot(share_pct, scenario_table["precision_at_share"], marker="o", label="Precision", color="#5B8FF9")
    plt.plot(share_pct, scenario_table["recall_at_share"], marker="o", label="Recall", color="#5AD8A6")
    plt.xlabel("Target Share (%)")
    plt.ylabel("Metric Value")
    plt.title("Scenario Check: Capacity vs Decision Metrics")
    plt.ylim(0, 1)
    plt.legend()
    _finalize_plot(output_path)
