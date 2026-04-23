from __future__ import annotations

import json
from pathlib import Path

from src.config import DEFAULT_DATASET_NAME, NOTEBOOKS_DIR, PROACTIVE_EXCLUDED_COLUMNS


def build_final_notebook(dataset_name: str = DEFAULT_DATASET_NAME) -> Path:
    notebook_path = NOTEBOOKS_DIR / "99_final_reproducible_notebook.ipynb"
    excluded = ", ".join(PROACTIVE_EXCLUDED_COLUMNS)

    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# NovaBank Final Reproducible Notebook\n",
                "\n",
                "This notebook reproduces the first-pass analytics workflow for the NovaBank proactive outreach project.\n",
                "\n",
                f"Modeling scope note: the pipeline excludes current-campaign contact-time fields (`{excluded}`) so the ranking stays aligned with a pre-contact prioritization decision.\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Workflow\n",
                "\n",
                "1. Load the dataset and profile the target.\n",
                "2. Apply the leakage-aware modeling frame.\n",
                "3. Train a logistic regression baseline and a gradient boosting model.\n",
                "4. Evaluate the top-20% targeting rule.\n",
                "5. Review trade-offs, explainability, defensibility, and scenarios.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "import sys\n",
                "\n",
                "PROJECT_ROOT = Path.cwd().resolve().parents[0] if Path.cwd().name == 'notebooks' else Path.cwd().resolve()\n",
                "if str(PROJECT_ROOT) not in sys.path:\n",
                "    sys.path.insert(0, str(PROJECT_ROOT))\n",
                "\n",
                "from src.reporting.pipeline import run_first_pass_analysis\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                f"results = run_first_pass_analysis(dataset_name='{dataset_name}')\n",
                "results['dataset_summary']\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Proxy Framing And Assumptions\n",
                "\n",
                "These tables make the project framing explicit for reviewers before the decision outputs.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from IPython.display import display\n",
                "\n",
                "display(results['proxy_target_framing'])\n",
                "display(results['assumptions_and_risks'])\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "results['target_definition']\n",
                "results['cleaning_decisions']\n",
                "results['split_summary']\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "results['baseline_results']\n",
                "results['improved_results']\n",
                "results['model_comparison']\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "results['decision_summary']\n",
                "results['targeting_summary']\n",
                "results['tradeoffs']\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "results['driver_summary']\n",
                "results['segment_sanity']\n",
                "results['scenario_analysis']\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Generated assets\n",
                "\n",
                "The pipeline also writes stable tables to `outputs/tables`, figures to `outputs/figures`, and reusable artifacts to `outputs/artifacts`.\n",
            ],
        },
    ]

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    notebook_path.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
    return notebook_path
