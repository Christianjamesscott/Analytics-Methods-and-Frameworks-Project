from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import TABLES_DIR, ensure_runtime_directories
from src.data.load_data import build_modeling_frame, list_available_datasets, load_dataset, resolve_dataset_path
from src.data.profile_data import (
    build_data_dictionary,
    build_dataset_summary,
    build_profile_summary,
    build_target_balance_table,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build starter profile outputs for NovaBank data.")
    parser.add_argument(
        "--dataset",
        choices=list_available_datasets(),
        default="bank",
        help="Dataset variant to profile.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_runtime_directories()

    frame = load_dataset(args.dataset)
    modeling_frame = build_modeling_frame(frame)
    profile = build_profile_summary(frame)
    dictionary = build_data_dictionary(frame)
    dataset_summary = build_dataset_summary(
        frame=frame,
        dataset_name=args.dataset,
        dataset_path=resolve_dataset_path(args.dataset),
        modeling_frame=modeling_frame,
    )
    target_balance = build_target_balance_table(frame)

    profile_path = TABLES_DIR / "table_data_profile_summary.csv"
    dictionary_path = TABLES_DIR / "table_data_dictionary.csv"
    dataset_summary_path = TABLES_DIR / "table_dataset_summary.csv"
    target_balance_path = TABLES_DIR / "table_target_balance.csv"

    profile.to_csv(profile_path, index=False)
    dictionary.to_csv(dictionary_path, index=False)
    dataset_summary.to_csv(dataset_summary_path, index=False)
    target_balance.to_csv(target_balance_path, index=False)

    print(f"Saved profile summary to {profile_path}")
    print(f"Saved data dictionary to {dictionary_path}")
    print(f"Saved dataset summary to {dataset_summary_path}")
    print(f"Saved target balance table to {target_balance_path}")


if __name__ == "__main__":
    main()
