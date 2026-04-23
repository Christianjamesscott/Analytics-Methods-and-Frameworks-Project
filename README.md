# NovaBank Analytics Project

This repo is for the NovaBank analytics lane only.

## Start here

Read the root operating documents in this order:

1. `AGENTS.md`
2. `CODEX_STARTUP_NOVABANK.md`
3. `OUTCOMES.md`
4. `SLIDES_AND_SUPPORTING_ARTIFACTS.md`

These documents define the scope, outcome standard, and downstream artifact expectations. The repo is intentionally not for memo writing, slide writing, or presentation design.

## Active analytics scope

- Profile and prepare the bank marketing dataset
- Build a logistic regression baseline
- Build one improved non-linear model
- Evaluate the top-20% outreach targeting rule
- Produce reproducible tables, figures, saved artifacts, and a final notebook

## Current dataset state

The raw dataset has been extracted into:

- `data/raw/uci_bank_marketing/bank/bank-full.csv`
- `data/raw/uci_bank_marketing/bank-additional/bank-additional/bank-additional-full.csv`

The first pass defaults to the `bank-full.csv` variant because it is the simpler starting point. That choice is controlled in [src/config.py](src/config.py).

## Modeling guardrail

For the proactive-outreach framing, the current first-pass model excludes variables tied to the last contact in the current campaign:

- `contact`
- `day`
- `month`
- `duration`
- `campaign`

This is deliberate leakage control. The repo is framed around pre-contact prioritization, not post-contact outcome explanation.

## Validated run path

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

The main entrypoint is [scripts/run_first_pass.py](scripts/run_first_pass.py). It builds the full first-pass output set and regenerates the final notebook.

## Current verified first pass

On the current verified run using `bank-full.csv` and the leakage-aware feature set:

- `gradient_boosting` ranked above `logistic_regression`
- top-20% precision was `0.2996` for `gradient_boosting`
- top-20% recall was `0.5123` for `gradient_boosting`

These values come from [table_model_comparison.csv](outputs/tables/table_model_comparison.csv).

## Repo map

```text
data/
  raw/        source files used for analysis
  processed/  regenerated modeling-frame files
docs/
notebooks/    final reproducible notebook output
outputs/
  tables/     stable csv deliverables
  figures/    reusable png visuals
  artifacts/  regenerated models, metadata, and scored test outputs
scripts/      runnable entrypoints
src/          reusable analytics modules
```

## Useful files

- [src/config.py](src/config.py): project constants, dataset paths, targeting share, and excluded columns
- [src/reporting/pipeline.py](src/reporting/pipeline.py): end-to-end first-pass orchestration
- [notebooks/99_final_reproducible_notebook.ipynb](notebooks/99_final_reproducible_notebook.ipynb): generated notebook that reuses the same pipeline
- [outputs/tables](outputs/tables): current reusable analytics tables
- [outputs/figures](outputs/figures): current reusable figures

## What exists now

- Raw data is unpacked
- Project folders exist
- Core modules exist for profiling, leakage-aware preprocessing, modeling, evaluation, explainability, defensibility checks, scenarios, and reporting
- Stable first-pass outputs have been generated
- A final reproducible notebook file exists

## What does not exist yet

- Finished business write-up
- Final memo/slide writing
- Any second-pass model tuning beyond the current passing-oriented workflow
