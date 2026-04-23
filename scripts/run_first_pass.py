from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting.notebook import build_final_notebook
from src.reporting.pipeline import run_first_pass_analysis


def main() -> None:
    results = run_first_pass_analysis()
    notebook_path = build_final_notebook()

    print("First-pass analytics pipeline completed.")
    print(f"Selected model: {results['selected_model_name']}")
    print(f"Saved final notebook to {notebook_path}")


if __name__ == "__main__":
    main()
