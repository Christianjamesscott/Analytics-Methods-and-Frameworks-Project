# NovaBank Analytics Project

This repo contains the analytics work for the NovaBank project. The analysis builds a proactive outreach prioritization framework using the provided bank marketing dataset as a proxy decision dataset. The current recommendation is to use gradient boosting and target the top 20% highest-scoring customers.

## Start Here / For Graders

- [Final reproducible notebook](notebooks/99_final_reproducible_notebook.ipynb)
- [Model comparison table](outputs/tables/table_model_comparison.csv)
- [Decision summary table](outputs/tables/table_decision_summary.csv)
- [Trade-off table](outputs/tables/table_tradeoffs.csv)
- [Scenario analysis table](outputs/tables/table_scenario_analysis.csv)
- [Assumptions and risks table](outputs/tables/table_assumptions_and_risks.csv)
- [Proxy framing table](outputs/tables/table_proxy_target_framing.csv)
- [Pilot plan inputs table](outputs/tables/table_pilot_plan_inputs.csv)
- [AI usage log](outputs/tables/table_ai_usage_log.csv)

## Project At A Glance

- Dataset used: UCI bank marketing dataset, used as a proxy prioritization framework for NovaBank outreach decisions
- Baseline model: logistic regression
- Improved model: gradient boosting
- Targeting rule: rank customers by score and target the top 20%
- Main recommendation: use the gradient boosting model to prioritize the top 20% highest-scoring customers for proactive outreach
- Major limitation: the dataset is not literal NovaBank churn or retention history, so this should be read as a prototype decision framework

## Key Outputs

- Notebook: [99_final_reproducible_notebook.ipynb](notebooks/99_final_reproducible_notebook.ipynb)
- Tables: [table_model_comparison.csv](outputs/tables/table_model_comparison.csv), [table_decision_summary.csv](outputs/tables/table_decision_summary.csv), [table_tradeoffs.csv](outputs/tables/table_tradeoffs.csv), [table_scenario_analysis.csv](outputs/tables/table_scenario_analysis.csv), [table_assumptions_and_risks.csv](outputs/tables/table_assumptions_and_risks.csv), [table_proxy_target_framing.csv](outputs/tables/table_proxy_target_framing.csv)
- Figures: [fig_model_comparison.png](outputs/figures/fig_model_comparison.png), [fig_feature_importance.png](outputs/figures/fig_feature_importance.png), [fig_scenario_comparison.png](outputs/figures/fig_scenario_comparison.png)

## Current Verified First Pass

On the current verified run using `bank-full.csv` and the leakage-aware feature set:

- `gradient_boosting` ranked above `logistic_regression`
- top-20% precision was `0.2996` for `gradient_boosting`
- top-20% recall was `0.5123` for `gradient_boosting`

These values come from [table_model_comparison.csv](outputs/tables/table_model_comparison.csv).

## Reproducibility

From the project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_first_pass.py
```

Optional notebook tooling:

```powershell
pip install -r requirements-notebook.txt
```

The main entrypoint is [scripts/run_first_pass.py](scripts/run_first_pass.py). It regenerates the first-pass outputs and final notebook.

## Internal Project Docs

These documents remain in the repo for project operating context:

- [AGENTS.md](AGENTS.md)
- [CODEX_STARTUP_NOVABANK.md](CODEX_STARTUP_NOVABANK.md)
- [OUTCOMES.md](OUTCOMES.md)
- [SLIDES_AND_SUPPORTING_ARTIFACTS.md](SLIDES_AND_SUPPORTING_ARTIFACTS.md)
