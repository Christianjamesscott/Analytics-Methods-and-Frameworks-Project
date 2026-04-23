# SLIDES_AND_SUPPORTING_ARTIFACTS.md

# NovaBank Slides and Supporting Artifacts Outline

## Purpose

This file does **not** ask Codex to write slide copy.

It exists so the analytics repo stays aware of the downstream presentation needs.
Codex should produce the tables, charts, and summaries that will later make the slide deck easy to assemble.

The final submission needs:
- one-page executive memo
- slide appendix
- notebook link

This file only covers what analytics outputs should exist to support the slide appendix and memo-building process.

---

## Slide outline target

Use this as the default slide structure to support later packaging.

The final deck should likely land around 8-10 slides.
The analytics repo should be able to support each slide below.

### Slide 1 — Business problem and decision
Purpose:
- explain what NovaBank is trying to decide
- frame the analysis around proactive outreach prioritization

Codex should provide:
- one short problem statement
- one short decision statement
- one simple KPI or decision framing note

Needed artifact types:
- plain-language summary bullets in notebook comments
- optional one-box problem framing figure if useful

---

### Slide 2 — Data and target framing
Purpose:
- show what dataset was used
- explain how the target was defined
- keep the framing simple and defensible

Codex should provide:
- compact dataset summary table
- target definition note
- train/test split summary

Needed artifact types:
- dataset overview table
- target balance table or chart
- short data dictionary excerpt

---

### Slide 3 — Baseline model
Purpose:
- show the starting point
- demonstrate that the project used a baseline rather than jumping straight to a stronger model

Codex should provide:
- baseline model name
- baseline performance metrics
- one simple interpretation note

Needed artifact types:
- baseline results table
- baseline confusion matrix or other simple performance visual
- optional coefficient summary excerpt

---

### Slide 4 — Improved model
Purpose:
- show the stronger model
- explain why it was considered better or more useful

Codex should provide:
- improved model name
- improved model performance metrics
- one short summary of what changed relative to baseline

Needed artifact types:
- improved model results table
- side-by-side comparison table
- optional PR/ROC chart if clean and readable

---

### Slide 5 — Decision rule: target the top 20%
Purpose:
- translate modeling into action
- show the actual targeting rule

Codex should provide:
- explicit top-20% rule
- number of customers selected
- selection logic
- precision/recall/capture for the targeted group

Needed artifact types:
- top-20% targeting table
- simple ranked-decile or percentile chart if useful
- short recommendation summary

---

### Slide 6 — Trade-off analysis
Purpose:
- show the consequence of acting on the model
- make false positives vs false negatives understandable

Codex should provide:
- false positive vs false negative comparison
- short business interpretation
- note on why the chosen rule is acceptable

Needed artifact types:
- trade-off table
- optional confusion-matrix visual or callout graphic
- short written interpretation in notebook comments

---

### Slide 7 — Explainability / defensibility
Purpose:
- make the recommendation understandable to non-technical stakeholders
- show that the prioritization is not a black box with no explanation

Codex should provide:
- top drivers from baseline
- top drivers from improved model
- one short defensibility note
- one small segment sanity check if possible

Needed artifact types:
- coefficient summary or odds-ratio table
- feature importance chart
- simple segment comparison table
- short limitations note

---

### Slide 8 — Scenario / sensitivity check
Purpose:
- show whether the recommendation is stable
- prove the decision does not collapse under one small variation

Codex should provide:
- one simple scenario analysis
- what changed
- what stayed the same

Needed artifact types:
- scenario comparison table
- optional one chart
- short stability summary

---

### Slide 9 — Final recommendation and pilot plan
Purpose:
- state the recommendation clearly
- show how NovaBank could test it operationally

Codex should provide:
- one recommendation summary
- pilot structure inputs
- KPI suggestion
- key risks or assumptions

Needed artifact types:
- recommendation summary bullets
- pilot plan skeleton
- assumptions / risks list

---

### Slide 10 — AI usage / appendix note
Purpose:
- if needed, make it easy for the final human-authored deck to note AI-supported workflow

Codex should provide:
- a concise log of where AI supported analytics work
- no overlong narrative

Needed artifact types:
- simple AI usage log
- dated notes or task list if available

---

## Supporting artifact checklist

The analytics repo should try to leave behind the following reusable artifacts because they make slide assembly much easier.

### Tables
- [ ] dataset summary table
- [ ] target balance table
- [ ] data dictionary excerpt table
- [ ] baseline results table
- [ ] improved results table
- [ ] baseline vs improved comparison table
- [ ] top-20% targeting table
- [ ] false positive vs false negative trade-off table
- [ ] scenario comparison table
- [ ] segment sanity-check table
- [ ] assumptions / risks list
- [ ] pilot plan skeleton
- [ ] AI usage log

### Figures
- [ ] target distribution chart
- [ ] one simple baseline performance visual
- [ ] one simple improved model performance visual
- [ ] one feature importance or explanation visual
- [ ] one scenario/sensitivity visual if useful

Do not create charts just to create charts.
Only keep visuals that are clean enough to be presentation-ready with light editing.

---

## Artifact quality standard

Each saved artifact should meet these rules:

1. It has a clear title.
2. Labels are readable.
3. It can stand alone with minimal extra explanation.
4. It is saved with a stable filename.
5. It is easy to reuse later in slides or memo drafting.

Avoid artifact sprawl.
Prefer a smaller set of reusable artifacts over many half-useful outputs.

---

## Naming convention suggestion

Use stable names in the outputs directory, for example:

### Tables
- `table_dataset_summary.csv`
- `table_target_balance.csv`
- `table_baseline_results.csv`
- `table_improved_results.csv`
- `table_model_comparison.csv`
- `table_top20_targeting.csv`
- `table_tradeoffs.csv`
- `table_scenario_analysis.csv`
- `table_segment_sanity_check.csv`
- `table_pilot_plan_inputs.csv`
- `table_ai_usage_log.csv`

### Figures
- `fig_target_distribution.png`
- `fig_baseline_performance.png`
- `fig_improved_performance.png`
- `fig_feature_importance.png`
- `fig_scenario_comparison.png`

Use another naming scheme if needed, but keep it consistent.

---

## Guardrail

Codex should treat this file as downstream context only.

This file does **not** expand the repo scope into:
- writing the slide deck
- writing the memo
- polishing visual design
- making presentation style choices

It only means the repo should leave behind the right evidence and reusable outputs so later human-authored deliverables are easy to build.

---

## Minimum viable slide support standard

If time gets tight, the repo must still be able to support these five core presentation needs:

1. What problem is being solved
2. What data and target were used
3. What baseline and improved model showed
4. What the top-20% decision rule is
5. What trade-off and scenario evidence support the recommendation

Everything else can be lighter if needed.
