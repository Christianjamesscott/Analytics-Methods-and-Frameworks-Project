# OUTCOMES.md

# NovaBank Codex Definition of Done

## Purpose

This file defines the required outcome state for the Codex analytics repo.

It is a validation target, not a brainstorming document.

The repo is considered complete for the analytics lane only when it can support:
- a clear recommendation on who NovaBank should prioritize
- a defensible top-20% outreach rule
- a baseline vs improved model comparison
- a false positive vs false negative trade-off discussion
- a simple scenario/sensitivity check
- a reproducible notebook that another reviewer can run and inspect

This repo does **not** need to write the executive memo, build the slides, or handle final submission packaging.

---

## Primary success condition

The analytics work is done when the repo can support a statement in this shape:

> NovaBank should proactively target the top 20% highest-scoring customers for outreach.
> This recommendation is supported by a baseline model, one improved model, explicit trade-off analysis, a light explainability layer, and one simple sensitivity check.

The exact wording can change later.
The analytics must be strong enough to support that recommendation.

---

## Required outputs

All of the following should exist before the analytics lane is treated as complete.

### 1. Data understanding outputs
- dataset intake summary
- compact data profile
- short data dictionary
- target definition
- train/test split description
- short note on cleaning/preprocessing decisions

### 2. Modeling outputs
- one baseline model
- one improved model
- reusable preprocessing pipeline
- reusable training/evaluation code
- saved model comparison results

### 3. Decision outputs
- explicit top-20% targeting rule
- targeting table showing how many customers are selected
- decision summary connecting model score to business action

### 4. Trade-off outputs
- false positive vs false negative table
- short interpretation in business language
- statement of the practical downside of the chosen rule

### 5. Explainability outputs
- simple explanation artifact for the baseline
- simple explanation artifact for the improved model
- short plain-language summary of main drivers

### 6. Stability / sensitivity outputs
- one scenario or sensitivity analysis
- concise statement of what changes and what holds

### 7. Reproducibility outputs
- one final reproducible notebook
- saved tables
- saved figures
- clear rerun path
- clean project structure

---

## Minimum acceptable technical shape

The repo should include, at minimum:

- raw data source or load path
- processed data logic or processed dataset
- train/test split logic
- baseline model code
- improved model code
- evaluation code
- targeting logic
- scenario logic
- one final notebook
- README or short run instructions

The repo does not need to be a polished software product.
It does need to be organized enough that a reviewer can follow it.

---

## Minimum acceptable analysis shape

The analysis is not complete if it stops at model training.

At minimum, the completed analysis must show:

1. what the target is
2. what the baseline model did
3. what the improved model did
4. whether the improved model is actually useful
5. how the top 20% are selected
6. what the false positive / false negative trade-off looks like
7. whether the recommendation is reasonably stable
8. why the recommendation is understandable enough to defend

---

## Pass-oriented standard

This project is intentionally narrow.

The goal is not to build the most advanced possible model.
The goal is to produce a simple, complete, business-linked analytics package that clears the assignment requirements cleanly.

A passing-oriented analytics package should be:

- narrow
- explicit
- reproducible
- decision-linked
- understandable

Avoid:
- extra model families unless necessary
- deep hyperparameter rabbit holes
- synthetic complexity for its own sake
- detached technical analysis with no decision consequence

---

## Validation checklist

The repo can be treated as analytically complete only if all boxes below can honestly be checked.

### Core analytics
- [ ] The target is clearly defined.
- [ ] The data was profiled and split properly.
- [ ] A baseline model exists.
- [ ] One improved model exists.
- [ ] Baseline and improved results are compared directly.

### Decision linkage
- [ ] The business action is explicit: target the top 20% for proactive outreach.
- [ ] The targeting rule is reproducible.
- [ ] A table exists showing the selected group and relevant performance.

### Trade-offs and defensibility
- [ ] False positives and false negatives are translated into business terms.
- [ ] One simple sensitivity/scenario test exists.
- [ ] There is at least a light explainability layer.
- [ ] There is a small defensibility check or segment sanity check.

### Reproducibility
- [ ] A final notebook exists.
- [ ] The notebook runs in a coherent sequence.
- [ ] Key tables and figures are saved to disk.
- [ ] The repo has enough structure for another person to review it.

---

## Non-goals

The following are explicitly out of scope for this repo outcome:

- writing the 1-page executive memo
- writing slide copy
- final citation formatting
- final PDF assembly
- hosting and submission logistics
- building a complex production-grade ML system

Those can be handled outside the analytics repo.

---

## Failure conditions

Do not mark the analytics lane complete if any of the following are true:

- only one model was trained and no baseline comparison exists
- there is no clear top-20% decision rule
- the analysis never translates into a business action
- there is no false positive vs false negative discussion
- there is no scenario/sensitivity check
- the repo cannot be rerun cleanly
- the outputs are too scattered to support later memo/slide creation

---

## Working rule

If time or scope pressure appears, preserve completeness over cleverness.

That means:
- keep the baseline
- keep one improved model
- keep the top-20% rule
- keep the trade-off table
- keep one scenario test
- keep the final notebook

Those are the core outcomes.
