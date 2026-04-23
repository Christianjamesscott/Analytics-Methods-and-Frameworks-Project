# NovaBank Codex Startup Guide

## Purpose

This file is the startup brief for the Codex project and main agent that will perform the **analytics work only** for the NovaBank project.

The goal is to keep the project narrow, direct, and passing-oriented. The agent should focus on building a clean, defensible analytics workflow that supports a later memo and slide deck, but it should **not** spend time writing those deliverables.

---

## Scope

### In scope
- Data loading, profiling, cleaning, and train/test split
- Baseline model
- One improved model
- Threshold selection tied to one business action
- Trade-off analysis
- Light explainability
- One simple scenario/sensitivity test
- Reproducible outputs
- Final notebook that can be linked in the project submission

### Out of scope
- Writing the executive memo
- Writing slide text
- Citation formatting
- Academic integrity writeups
- Presentation design
- Building an unnecessarily complex ML system
- Multi-policy optimization unless needed to support the chosen recommendation

---

## Project framing

Use the **NovaBank** example project.

Treat the provided bank marketing dataset as a **practical proxy** for proactive retention / outreach prioritization.

Do **not** try to force a full churn dataset interpretation if the data does not naturally support it.

The working framing is:

> NovaBank wants to move from reactive outreach to proactive outreach.  
> The analytics task is to identify which customers should be prioritized for intervention first.

This is the simplest defensible path.

---

## Single business action to optimize for

Optimize for **one action only**:

> **Target the top 20% highest-scoring customers for proactive outreach.**

Do not branch into multiple strategy tracks unless the analysis breaks and requires it.

The point of the project is not to prove every possible policy. The point is to support one reasonable decision with evidence.

---

## Core decision question

The main decision question is:

> Which customers should NovaBank prioritize for proactive outreach if it can only focus on the top 20% of customers based on model scores?

Every major modeling and evaluation choice should support that question.

---

## Modeling philosophy

Keep the workflow straightforward.

1. Start with a clean baseline.
2. Build one improved model.
3. Compare them.
4. Pick a threshold or top-k rule tied to the business action.
5. Show trade-offs.
6. Show a minimal explainability layer.
7. Run one simple sensitivity/scenario test.
8. Save outputs in a reusable, reproducible way.

Do not overengineer.  
Do not chase tiny performance gains if they do not improve the decision.

---

## Assumptions to use unless the code or data forces a change

Use these assumptions by default and clearly log them in the project.

### Dataset framing assumption
The provided bank marketing response outcome is used as a proxy for identifying customers who should be prioritized for proactive outreach.

### Intervention capacity assumption
NovaBank has enough capacity to proactively contact **20% of customers**.

### Decision assumption
Higher model scores mean higher priority for outreach.

### Error trade-off assumption
False negatives are somewhat worse than false positives, but not by an extreme amount.  
Practical interpretation:
- False positive = outreach spent on someone who was not a strong priority
- False negative = missed opportunity to intervene with someone who should have been prioritized

### Defensibility assumption
Recommendations should be transparent and understandable to non-technical stakeholders.

### Complexity assumption
Use minimal dependencies unless extra libraries are clearly needed.

If any assumption has to change, document the reason in the notebook and outputs.

---

## Required analytics outputs

The project must leave behind analytics artifacts that later support the memo and slides.

At minimum produce:

1. Data profile summary
2. Data dictionary
3. Train/test split description
4. Baseline model results table
5. Improved model results table
6. Top-20% targeting table
7. Confusion-matrix-based trade-off table
8. One scenario/sensitivity table
9. One explainability output for the baseline
10. One explainability output for the improved model
11. Final reproducible notebook
12. Saved figures and tables in the outputs directory

---

## Success standard for this Codex project

This project is optimized to **pass cleanly**, not to become a giant capstone-grade ML platform.

A successful outcome for this repo is:

- there is a clear business framing
- the data is cleaned and profiled
- there is a proper train/test split
- there is a baseline model
- there is one improved model
- there is a clear comparison
- there is a recommendation tied to targeting the top 20%
- there is some discussion of false positives vs false negatives
- there is one simple scenario/sensitivity test
- there is some explainability
- there is a reproducible final notebook

If those are done clearly, the project is in good shape.

---

## Recommended technical stack

Default to:

- Python
- pandas
- numpy
- scikit-learn
- matplotlib
- jupyter

Only add packages such as `shap`, `xgboost`, or `lightgbm` if they are clearly needed and justified.

Prefer the simplest stack that gets the job done.

---

## Recommended repo structure

Use this structure or something close to it.

```text
novabank-project/
  data/
    raw/
    processed/
  notebooks/
    01_data_profile.ipynb
    02_baseline_model.ipynb
    03_improved_model.ipynb
    04_thresholds_and_scenarios.ipynb
    99_final_reproducible_notebook.ipynb
  src/
    data/
      load_data.py
      clean_data.py
      split_data.py
    features/
      build_features.py
    models/
      train_baseline.py
      train_improved.py
      predict.py
    evaluation/
      metrics.py
      thresholds.py
      explainability.py
      plots.py
    scenarios/
      run_scenarios.py
  outputs/
    tables/
    figures/
    artifacts/
  docs/
    notes.md
  requirements.txt
  README.md
```

Keep the code modular enough to rerun.  
Do not bury everything inside one giant notebook.

---

## Recommended model choices

### Baseline model
Start with **logistic regression**.

Why:
- simple
- explainable
- standard
- good benchmark
- easy to defend in a business analytics project

### Improved model
Use **tree-based boosting or another simple non-linear classifier**, but only one.

Recommended default order:
1. Gradient boosting classifier
2. Random forest if boosting becomes annoying
3. XGBoost only if justified and dependency cost is acceptable

The improved model only needs to be meaningfully better or differently useful than the baseline. It does not need to be state-of-the-art.

---

## Evaluation approach

The project is about prioritization, not just raw classification.

Use a metric set that supports prioritization.

### Primary evaluation focus
- precision in the top 20%
- recall in the top 20%
- actual capture in the targeted population

### Supporting metrics
- PR AUC
- ROC AUC
- confusion matrix at chosen threshold / top-k rule
- calibration check if easy to do

### Do not rely on
- raw accuracy alone
- overly abstract technical metrics with no business interpretation

---

## Threshold / targeting rule

The default policy is:

> Rank customers by model score and target the top 20%.

This can be implemented as:
- percentile-based ranking, or
- threshold chosen to roughly select the top 20%

Whichever is cleaner is fine.  
The main requirement is that the rule is explicit and reproducible.

The final recommendation should clearly state:
- who gets targeted
- how they are selected
- why this rule is preferred

---

## Light explainability requirement

This does **not** need to become a giant explainable-AI project.

Keep it practical.

### Baseline model explainability
- coefficient table or odds-ratio style summary
- plain-language explanation of the strongest drivers

### Improved model explainability
- feature importance plot
- permutation importance or SHAP only if easy and worth it
- short summary of top drivers

The output should be understandable enough that a non-technical stakeholder can see why the model prioritizes some customers above others.

---

## Light defensibility / fairness check

Keep this small.

This project does **not** need a full fairness workstream.

Do one simple defensibility check such as:
- compare predicted positive rates or top-20% selection rates across a few major segments
- compare performance across a few major customer groups if the variables support it

Examples of candidate grouping variables:
- age buckets
- job category
- marital status
- education level
- loan-related fields

Do not overstate fairness claims.  
Just provide a small sanity check and note limitations.

---

## Scenario / sensitivity test

Run **one** simple scenario test.

Preferred default options, in order:

1. Vary intervention capacity:
   - top 10%
   - top 20%
   - top 30%

2. Vary error-cost assumptions:
   - false negative slightly worse
   - false negative clearly worse

3. Vary threshold stability:
   - compare recommendation stability around nearby cutoffs

Use whichever is easiest to implement cleanly.

The goal is to show:
- what holds
- what shifts
- whether the recommendation is stable

Keep this simple.

---

## Expected workflow

Follow this order.

### Phase 1: Data intake and profiling
Tasks:
- load raw data
- inspect shape, columns, dtypes
- inspect target balance
- inspect missingness
- inspect duplicates
- identify obvious cleaning needs
- create a short data dictionary

Deliverables:
- profiling notebook or script output
- data dictionary table
- cleaned dataset candidate

### Phase 2: Data preparation
Tasks:
- clean obvious issues
- encode categorical features
- define target
- split train/test properly
- prevent leakage
- create preprocessing pipeline

Deliverables:
- reusable preprocessing code
- saved train/test objects or reproducible split logic

### Phase 3: Baseline model
Tasks:
- train logistic regression
- evaluate on test set
- save metrics
- save plots/tables
- summarize drivers

Deliverables:
- baseline results table
- confusion matrix
- PR/ROC visual
- baseline explanation output

### Phase 4: Improved model
Tasks:
- train one stronger model
- evaluate on test set
- compare with baseline
- capture main differences

Deliverables:
- improved results table
- comparison table
- improved model explanation output

### Phase 5: Decision rule and top-20% targeting
Tasks:
- rank customers by model score
- isolate top 20%
- measure precision/recall/capture for that selected group
- create recommendation table

Deliverables:
- targeting table
- top-20% performance summary
- recommended business rule

### Phase 6: Trade-off analysis
Tasks:
- translate errors into business terms
- compare false positives vs false negatives
- show practical consequence of the chosen rule

Deliverables:
- trade-off table
- concise written interpretation in notebook comments

### Phase 7: Scenario / sensitivity
Tasks:
- run one simple scenario test
- compare outputs
- note what changes and what stays stable

Deliverables:
- scenario comparison table
- one chart if useful

### Phase 8: Final assembly
Tasks:
- consolidate results
- create one final reproducible notebook
- save clean outputs for later memo/slide use
- confirm rerun path works

Deliverables:
- `99_final_reproducible_notebook.ipynb`
- saved figures
- saved tables
- clean README

---

## Concrete deliverable checklist

Before calling the analytics work complete, verify that the repo contains:

- [ ] raw dataset
- [ ] processed dataset or reproducible processing logic
- [ ] data dictionary
- [ ] train/test split logic
- [ ] baseline model code
- [ ] improved model code
- [ ] model comparison table
- [ ] top-20% targeting rule
- [ ] trade-off table
- [ ] one scenario/sensitivity test
- [ ] baseline explainability output
- [ ] improved model explainability output
- [ ] light defensibility check
- [ ] final reproducible notebook
- [ ] output figures and tables saved to disk

---

## Guardrails for the main agent

The agent should follow these rules.

1. **Do the simplest valid thing first.**
2. **Do not overcomplicate the dataset framing.**
3. **Do not invent extra project requirements.**
4. **Do not spend time on memo or slide writing.**
5. **Do not optimize for academic style; optimize for clean analytics outputs.**
6. **Keep code modular and rerunnable.**
7. **Document assumptions briefly but clearly.**
8. **If a choice is ambiguous, prefer the more defensible and simpler option.**
9. **If model performance differences are small, prefer the more explainable model unless the improved model materially changes the decision quality.**
10. **If a requested analysis becomes a rabbit hole, stop and return to the core decision question.**

---

## What the final recommendation should eventually look like

The project should be capable of supporting a final statement close to this:

> NovaBank should proactively target the top 20% highest-scoring customers for outreach.  
> This rule is supported by model-based ranking, comparison against a baseline, explicit trade-off analysis, and a simple sensitivity check showing the recommendation is reasonably stable.

The exact wording can change later, but the analytics should support something in that shape.

---

## First-run task list for the agent

When starting the repo, do the following first:

1. Inspect the dataset and identify the target column.
2. Produce a compact profiling summary.
3. Draft a one-table data dictionary.
4. Build a preprocessing pipeline.
5. Train a logistic regression baseline.
6. Evaluate baseline with prioritization-focused metrics.
7. Train one improved model.
8. Compare baseline vs improved model.
9. Build a top-20% targeting table.
10. Create a false positive / false negative trade-off table.
11. Run one simple scenario test.
12. Save outputs and assemble a final notebook.

Do not skip directly to fancy modeling.

---

## Definition of done

This analytics project is done when:

- the repo can be rerun without manual chaos
- the model comparison is clear
- the top-20% targeting recommendation is explicit
- the trade-offs are visible
- the outputs are understandable
- there is one final notebook that someone else could review

That is enough.

