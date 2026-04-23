from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting.pipeline import run_first_pass_analysis


def main() -> None:
    results = run_first_pass_analysis()
    print("train_models.py now runs the full first-pass analytics pipeline.")
    print(f"Selected model: {results['selected_model_name']}")


if __name__ == "__main__":
    main()
