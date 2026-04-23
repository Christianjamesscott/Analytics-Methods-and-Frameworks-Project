from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd

from src.config import (
    ARTIFACTS_DIR,
    DEFAULT_DATASET_NAME,
    FIGURES_DIR,
    MODEL_SELECTION_RULE,
    PROACTIVE_EXCLUDED_COLUMNS,
    PROCESSED_DATA_DIR,
    RANDOM_STATE,
    SCENARIO_CAPACITIES,
    TABLES_DIR,
    TARGET_DEFINITION_NOTE,
    TEST_SIZE,
    TOP_K_SHARE,
    ensure_runtime_directories,
)
from src.data.load_data import build_modeling_frame, load_dataset, resolve_dataset_path
from src.data.profile_data import (
    build_cleaning_decisions_table,
    build_data_dictionary,
    build_dataset_summary,
    build_profile_summary,
    build_split_summary,
    build_target_balance_table,
    build_target_definition_table,
)
from src.data.split_data import create_train_test_split
from src.evaluation.defensibility import build_segment_sanity_table
from src.evaluation.explainability import (
    baseline_coefficient_table,
    build_driver_summary_table,
    feature_importance_table,
)
from src.evaluation.metrics import (
    build_comparison_table,
    build_decision_summary_table,
    build_model_results_table,
    build_tradeoff_table,
)
from src.evaluation.plots import (
    plot_feature_importance,
    plot_model_comparison,
    plot_precision_recall_curve_for_model,
    plot_scenario_comparison,
    plot_target_distribution,
)
from src.evaluation.thresholds import build_scored_ranking_table, build_targeting_summary_table
from src.models.common import ModelBundle, score_rows
from src.models.train_baseline import train_baseline_model
from src.models.train_improved import train_improved_model
from src.scenarios.run_scenarios import run_capacity_scenarios


def _table_path(name: str) -> Path:
    return TABLES_DIR / f"{name}.csv"


def _figure_path(name: str) -> Path:
    return FIGURES_DIR / f"{name}.png"


def _artifact_path(name: str) -> Path:
    return ARTIFACTS_DIR / name


def _save_table(name: str, frame: pd.DataFrame) -> Path:
    path = _table_path(name)
    frame.to_csv(path, index=False)
    return path


def _save_model_bundle(bundle: ModelBundle, name: str) -> Path:
    path = _artifact_path(name)
    joblib.dump(bundle, path)
    return path


def build_assumptions_risks_table(selected_model_name: str) -> pd.DataFrame:
    rows = [
        {
            "category": "dataset_framing",
            "item": "proxy_target",
            "note": TARGET_DEFINITION_NOTE,
        },
        {
            "category": "capacity",
            "item": "top20_rule",
            "note": "NovaBank is assumed to have enough outreach capacity to contact the top 20% of ranked customers.",
        },
        {
            "category": "model_scope",
            "item": "excluded_current_campaign_fields",
            "note": (
                "The model excludes contact-time variables tied to the current campaign: "
                + ", ".join(PROACTIVE_EXCLUDED_COLUMNS)
                + "."
            ),
        },
        {
            "category": "model_selection",
            "item": "selection_rule",
            "note": MODEL_SELECTION_RULE,
        },
        {
            "category": "risk",
            "item": "proxy_outcome_limitation",
            "note": "The target reflects term-deposit response, not a literal churn label, so business interpretation should stay within outreach prioritization.",
        },
        {
            "category": "risk",
            "item": "single_split_validation",
            "note": "This first pass uses one stratified train/test split rather than repeated resampling.",
        },
        {
            "category": "decision",
            "item": "selected_model",
            "note": f"The current recommended model is {selected_model_name} based on top-20% decision usefulness on the held-out test set.",
        },
    ]
    return pd.DataFrame(rows)


def build_pilot_plan_inputs_table(selected_model_name: str, targeting_summary: pd.DataFrame) -> pd.DataFrame:
    targeted_customers = int(targeting_summary.loc[0, "targeted_customers"])
    return pd.DataFrame(
        [
            {
                "pilot_item": "objective",
                "value": "Test whether model-ranked outreach improves conversion efficiency versus untargeted outreach.",
            },
            {
                "pilot_item": "recommended_model",
                "value": selected_model_name,
            },
            {
                "pilot_item": "target_population",
                "value": f"Top {int(TOP_K_SHARE * 100)}% highest-scoring customers in the scoring population.",
            },
            {
                "pilot_item": "pilot_batch_size",
                "value": str(targeted_customers),
            },
            {
                "pilot_item": "primary_kpi",
                "value": "Conversion rate within the targeted group.",
            },
            {
                "pilot_item": "secondary_kpi",
                "value": "Captured positives and outreach cost per conversion.",
            },
            {
                "pilot_item": "monitoring_note",
                "value": "Track false-positive burden and missed-opportunity risk if capacity is tightened below 20%.",
            },
        ]
    )


def build_ai_usage_log_table() -> pd.DataFrame:
    now = datetime.now().isoformat(timespec="seconds")
    rows = [
        {
            "timestamp": now,
            "workflow_stage": "repo_initialization",
            "ai_support": "Set up the project scaffold, local virtual environment, and starter analytics structure.",
        },
        {
            "timestamp": now,
            "workflow_stage": "dataset_preparation",
            "ai_support": "Extracted the bank marketing dataset and encoded the proactive-outreach feature exclusions.",
        },
        {
            "timestamp": now,
            "workflow_stage": "modeling_and_reporting",
            "ai_support": "Ran the first-pass baseline and improved models, saved outputs, and generated the reusable notebook.",
        },
    ]
    return pd.DataFrame(rows)


def _save_run_metadata(
    dataset_name: str,
    dataset_path: Path,
    selected_model_name: str,
    model_comparison: pd.DataFrame,
) -> Path:
    metadata = {
        "run_timestamp": datetime.now().isoformat(timespec="seconds"),
        "dataset_name": dataset_name,
        "dataset_path": str(dataset_path),
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "top_k_share": TOP_K_SHARE,
        "excluded_columns": PROACTIVE_EXCLUDED_COLUMNS,
        "selected_model": selected_model_name,
        "model_comparison": model_comparison.to_dict(orient="records"),
    }
    path = _artifact_path("artifact_run_metadata.json")
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return path


def run_first_pass_analysis(dataset_name: str = DEFAULT_DATASET_NAME) -> dict[str, object]:
    ensure_runtime_directories()

    dataset_path = resolve_dataset_path(dataset_name)
    raw_frame = load_dataset(dataset_name)
    modeling_frame = build_modeling_frame(raw_frame)

    processed_dataset_path = PROCESSED_DATA_DIR / f"{dataset_name}_modeling_frame.csv"
    modeling_frame.to_csv(processed_dataset_path, index=False)

    dataset_summary = build_dataset_summary(
        frame=raw_frame,
        dataset_name=dataset_name,
        dataset_path=dataset_path,
        modeling_frame=modeling_frame,
    )
    profile_summary = build_profile_summary(raw_frame)
    target_balance = build_target_balance_table(raw_frame)
    data_dictionary = build_data_dictionary(raw_frame)
    target_definition = build_target_definition_table()
    cleaning_decisions = build_cleaning_decisions_table(raw_frame)

    x_train, x_test, y_train, y_test = create_train_test_split(modeling_frame)
    split_summary = build_split_summary(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)

    baseline_bundle = train_baseline_model(x_train, y_train)
    improved_bundle = train_improved_model(x_train, y_train)

    baseline_scores = score_rows(baseline_bundle, x_test)
    improved_scores = score_rows(improved_bundle, x_test)

    baseline_results = build_model_results_table(
        name=baseline_bundle.name,
        y_true=y_test,
        scores=baseline_scores,
        share=TOP_K_SHARE,
    )
    improved_results = build_model_results_table(
        name=improved_bundle.name,
        y_true=y_test,
        scores=improved_scores,
        share=TOP_K_SHARE,
    )
    model_comparison = build_comparison_table(
        results={
            baseline_bundle.name: baseline_scores,
            improved_bundle.name: improved_scores,
        },
        y_true=y_test,
        share=TOP_K_SHARE,
    )

    selected_model_name = str(model_comparison.iloc[0]["model"])
    if selected_model_name == baseline_bundle.name:
        selected_scores = baseline_scores
    else:
        selected_scores = improved_scores

    targeting_summary = build_targeting_summary_table(
        model_name=selected_model_name,
        y_true=y_test,
        scores=selected_scores,
        share=TOP_K_SHARE,
    )
    scored_test = build_scored_ranking_table(
        features=x_test,
        y_true=y_test,
        scores=selected_scores,
        share=TOP_K_SHARE,
    )
    selected_customers = scored_test.loc[scored_test["selected_for_outreach"]].copy()

    decision_summary = build_decision_summary_table(
        model_name=selected_model_name,
        y_true=y_test,
        scores=selected_scores,
        share=TOP_K_SHARE,
    )
    tradeoffs = build_tradeoff_table(
        model_name=selected_model_name,
        y_true=y_test,
        scores=selected_scores,
        share=TOP_K_SHARE,
    )

    baseline_explainability = baseline_coefficient_table(baseline_bundle)
    improved_explainability = feature_importance_table(improved_bundle)
    driver_summary = build_driver_summary_table(
        baseline_table=baseline_explainability,
        improved_table=improved_explainability,
    )

    segment_sanity = build_segment_sanity_table(
        features=x_test,
        y_true=y_test,
        scores=selected_scores,
        share=TOP_K_SHARE,
        segment_column="age",
    )
    scenario_analysis = run_capacity_scenarios(
        y_true=y_test,
        scores=selected_scores,
        capacities=SCENARIO_CAPACITIES,
    )
    assumptions_risks = build_assumptions_risks_table(selected_model_name=selected_model_name)
    pilot_plan_inputs = build_pilot_plan_inputs_table(
        selected_model_name=selected_model_name,
        targeting_summary=targeting_summary,
    )
    ai_usage_log = build_ai_usage_log_table()

    saved_tables = {
        "dataset_summary": _save_table("table_dataset_summary", dataset_summary),
        "profile_summary": _save_table("table_data_profile_summary", profile_summary),
        "target_balance": _save_table("table_target_balance", target_balance),
        "data_dictionary": _save_table("table_data_dictionary", data_dictionary),
        "target_definition": _save_table("table_target_definition", target_definition),
        "split_summary": _save_table("table_train_test_split", split_summary),
        "cleaning_decisions": _save_table("table_cleaning_decisions", cleaning_decisions),
        "baseline_results": _save_table("table_baseline_results", baseline_results),
        "improved_results": _save_table("table_improved_results", improved_results),
        "model_comparison": _save_table("table_model_comparison", model_comparison),
        "decision_summary": _save_table("table_decision_summary", decision_summary),
        "targeting_summary": _save_table("table_top20_targeting", targeting_summary),
        "tradeoffs": _save_table("table_tradeoffs", tradeoffs),
        "baseline_explainability": _save_table("table_baseline_coefficients", baseline_explainability),
        "improved_explainability": _save_table("table_improved_feature_importance", improved_explainability),
        "driver_summary": _save_table("table_driver_summary", driver_summary),
        "segment_sanity": _save_table("table_segment_sanity_check", segment_sanity),
        "scenario_analysis": _save_table("table_scenario_analysis", scenario_analysis),
        "assumptions_risks": _save_table("table_assumptions_risks", assumptions_risks),
        "pilot_plan_inputs": _save_table("table_pilot_plan_inputs", pilot_plan_inputs),
        "ai_usage_log": _save_table("table_ai_usage_log", ai_usage_log),
        "selected_customers": _save_table("table_top20_selected_customers", selected_customers),
    }

    scored_test_path = _artifact_path("artifact_scored_test_set.csv")
    scored_test.to_csv(scored_test_path, index=False)
    baseline_model_path = _save_model_bundle(baseline_bundle, "artifact_baseline_model.joblib")
    improved_model_path = _save_model_bundle(improved_bundle, "artifact_improved_model.joblib")
    metadata_path = _save_run_metadata(
        dataset_name=dataset_name,
        dataset_path=dataset_path,
        selected_model_name=selected_model_name,
        model_comparison=model_comparison,
    )

    plot_target_distribution(target_balance=target_balance, output_path=_figure_path("fig_target_distribution"))
    plot_model_comparison(model_comparison=model_comparison, output_path=_figure_path("fig_model_comparison"))
    plot_precision_recall_curve_for_model(
        model_name=baseline_bundle.name,
        y_true=y_test,
        scores=baseline_scores,
        output_path=_figure_path("fig_baseline_precision_recall_curve"),
    )
    plot_precision_recall_curve_for_model(
        model_name=improved_bundle.name,
        y_true=y_test,
        scores=improved_scores,
        output_path=_figure_path("fig_improved_precision_recall_curve"),
    )
    plot_feature_importance(
        importance_table=improved_explainability,
        output_path=_figure_path("fig_feature_importance"),
        title="Improved Model Feature Importance",
    )
    plot_scenario_comparison(
        scenario_table=scenario_analysis,
        output_path=_figure_path("fig_scenario_comparison"),
    )

    return {
        "dataset_summary": dataset_summary,
        "profile_summary": profile_summary,
        "target_balance": target_balance,
        "data_dictionary": data_dictionary,
        "target_definition": target_definition,
        "split_summary": split_summary,
        "cleaning_decisions": cleaning_decisions,
        "baseline_results": baseline_results,
        "improved_results": improved_results,
        "model_comparison": model_comparison,
        "decision_summary": decision_summary,
        "targeting_summary": targeting_summary,
        "tradeoffs": tradeoffs,
        "baseline_explainability": baseline_explainability,
        "improved_explainability": improved_explainability,
        "driver_summary": driver_summary,
        "segment_sanity": segment_sanity,
        "scenario_analysis": scenario_analysis,
        "assumptions_risks": assumptions_risks,
        "pilot_plan_inputs": pilot_plan_inputs,
        "ai_usage_log": ai_usage_log,
        "selected_customers": selected_customers,
        "saved_tables": saved_tables,
        "saved_artifacts": {
            "processed_dataset": processed_dataset_path,
            "scored_test_set": scored_test_path,
            "baseline_model": baseline_model_path,
            "improved_model": improved_model_path,
            "run_metadata": metadata_path,
        },
        "selected_model_name": selected_model_name,
    }

