# AGENTS.md

This file adds **project-specific operating rules** for the NovaBank repo. It supplements the workspace-level custom instructions. If there is any conflict, follow:
1. the latest direct user instruction
2. the workspace-level custom instructions
3. this file

## Default active lane

Unless the user narrows scope further, the active lane for this repo is:

> **NovaBank analytics work only**

That means:
- data intake and profiling
- preprocessing
- baseline model
- one improved model
- top-20% targeting rule
- trade-off analysis
- light explainability
- one simple scenario / sensitivity test
- reproducible outputs and final notebook

## Explicitly out of scope by default

Do **not** drift into these areas unless the user explicitly asks:
- executive memo writing
- slide writing or slide design
- citations or academic-policy formatting
- AI-use disclosure writeups
- presentation polish
- broad product strategy unrelated to the analytics workflow
- extra modeling branches that do not improve the core decision
- capstone-style expansion

## Project framing

Use the **NovaBank** example project.

Treat the provided bank marketing dataset as a **proxy for proactive outreach prioritization**.

Do **not** force a literal churn dataset interpretation if the data does not support that cleanly.

Working framing:

> NovaBank wants to move from reactive outreach to proactive outreach. The analytics task is to identify which customers should be prioritized first.

## Locked project choices

These are already decided for this repo unless the user changes them.

### 1) Passing-oriented scope
Optimize for a clean pass, not a complex showcase project.

### 2) Single business action
Optimize for **one action only**:

> **Target the top 20% highest-scoring customers for proactive outreach.**

Do not branch into multiple policy paths unless the user asks or the analysis breaks.

### 3) Minimal dependency bias
Prefer:
- Python
- pandas
- numpy
- scikit-learn
- matplotlib
- Jupyter

Only add extra packages if they are clearly needed.

### 4) Build order
Prefer:
- scripts / modules first
- final reproducible notebook later

Do not hide everything inside one giant exploratory notebook.

### 5) Minimal defensibility check
Include a **small sanity-check section** so the recommendation is at least somewhat transparent and defensible.

This is not a full fairness project.

## Core decision question

Every major modeling choice should support this question:

> Which customers should NovaBank prioritize for proactive outreach if it can only focus on the top 20% of customers based on model score?

If work drifts away from that question, stop and return to it.

## Modeling philosophy

Keep the workflow simple and defensible:
1. profile the data
2. clean and preprocess it
3. build a baseline
4. build one improved model
5. compare them
6. implement the top-20% targeting rule
7. show false-positive vs false-negative trade-offs
8. add light explainability
9. run one simple scenario / sensitivity test
10. assemble reproducible outputs

Do not chase sophistication for its own sake.

## Default model choices

### Baseline
Use **logistic regression** first.

Reason:
- simple
- explainable
- standard benchmark
- easy to defend

### Improved model
Use **one** stronger non-linear model.
Preferred order:
1. Gradient boosting classifier
2. Random forest
3. XGBoost only if clearly justified

The improved model does not need to be fancy. It only needs to satisfy the project requirement for baseline + improved comparison and ideally improve decision usefulness.

## Evaluation rules

This project is about **prioritization**, not just generic classification.

### Primary focus
Use metrics that support the top-20% action, such as:
- precision within the top 20%
- recall / capture within the top 20%
- number of positives captured in the targeted segment

### Supporting metrics
Use only what helps explain the decision:
- PR AUC
- ROC AUC
- confusion matrix at the chosen rule
- calibration check if easy and useful

Do **not** lean on raw accuracy as the main story.

## Threshold / targeting rule

The default policy is:

> Rank customers by score and target the top 20%.

This can be implemented with:
- percentile ranking, or
- a threshold that selects about the top 20%

Choose the cleaner implementation.

The final analytics output must clearly show:
- who gets selected
- how selection is determined
- why the rule is reasonable

## Trade-off analysis

The analysis must explicitly translate errors into business terms.

Default interpretation:
- false positive = outreach spent on a weaker-priority customer
- false negative = missed opportunity to prioritize a stronger candidate for outreach

False negatives are assumed to be somewhat worse than false positives, but not by an extreme amount.

Keep the trade-off section concrete and narrow.

## Explainability requirement

Keep explainability practical.

### Baseline
Produce:
- coefficient summary or odds-ratio style summary
- short plain-language note on strongest drivers

### Improved model
Produce:
- feature importance
- permutation importance if useful
- SHAP only if easy and justified

Do not turn this into a large XAI project.

## Minimal defensibility check

Do one small defensibility sanity check if the variables support it.
Examples:
- compare top-20% selection rates across a few major segments
- compare model performance across a few simple groups

Candidate grouping variables may include:
- age buckets
- job
- marital status
- education
- loan-related flags

Do not make strong fairness claims. Just provide a small sanity check and a brief limitation note.

## Scenario / sensitivity test

Run **one** simple scenario test.
Preferred order:
1. vary outreach capacity: top 10%, 20%, 30%
2. vary error-cost assumptions
3. test nearby threshold stability

Keep this compact. The goal is to show whether the recommendation is directionally stable.

## Required outputs

The repo should produce at least these artifacts:
- data profile summary
- data dictionary
- train/test split description or reusable code
- baseline model results table
- improved model results table
- model comparison table
- top-20% targeting table
- false-positive / false-negative trade-off table
- one scenario / sensitivity table
- baseline explainability output
- improved model explainability output
- small defensibility check
- final reproducible notebook
- saved tables and figures in an outputs folder

## Preferred repo shape

A structure close to this is preferred:

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
    features/
    models/
    evaluation/
    scenarios/
  outputs/
    tables/
    figures/
    artifacts/
  docs/
  requirements.txt
  README.md
```

Do not force this exact layout if the repo already has a reasonable structure.

## Stop-and-ask triggers

Stop and ask the user before pushing ahead if any of these happen:
- the dataset is missing or materially different from expected
- the target variable is ambiguous in a way that changes the project framing
- there is a serious leakage concern that changes the validity of the approach
- the repo already has structural conventions that conflict with this file
- the simplest passing path is blocked and a more complex path would be required

If none of those are true, keep moving.

## Verification and claims

Do not claim more than was checked.

Only say something is done or verified when the claim is tightly scoped.
Examples:
- acceptable: “baseline model script runs end-to-end on the current dataset split”
- not acceptable: “the analytics workflow is solved”

Be precise about what was and was not tested.

## Default work sequence

Follow this order unless the user narrows scope:

### Phase 1 — Data profile
- inspect shape, columns, types, missingness, duplicates, target balance
- create a short data dictionary

### Phase 2 — Preparation
- clean obvious issues
- encode or preprocess features
- build a proper train/test split
- prevent leakage

### Phase 3 — Baseline
- train logistic regression
- evaluate with prioritization-focused metrics
- save results and explanation output

### Phase 4 — Improved model
- train one stronger model
- compare against baseline
- save results and explanation output

### Phase 5 — Decision rule
- rank customers by score
- isolate top 20%
- measure performance for that selected group
- produce recommendation table

### Phase 6 — Trade-offs
- translate FP and FN into business terms
- summarize the consequence of the chosen rule

### Phase 7 — Scenario test
- run one simple scenario or sensitivity test
- summarize what changes and what holds

### Phase 8 — Final assembly
- consolidate outputs
- assemble final reproducible notebook
- save reusable tables and figures

## Definition of done for this repo

This analytics work is in good shape when:
- the workflow reruns without chaos
- there is a baseline and one improved model
- the top-20% targeting rule is explicit
- trade-offs are visible
- the outputs are understandable
- there is one final notebook that someone else can review

That is enough.
