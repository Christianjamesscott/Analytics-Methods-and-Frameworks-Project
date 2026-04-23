# Outputs

Generated tables, figures, and artifacts are written here by the analytics pipeline.

## Naming convention

- `table_*`: reusable CSV outputs intended to support analysis review and later memo/slide assembly
- `fig_*`: reusable PNG visuals
- `artifact_*`: regenerated model files, metadata, and scored-output files used to support reruns and inspection

## Primary generator

Run `python scripts/run_first_pass.py` from the project root to refresh this directory.
