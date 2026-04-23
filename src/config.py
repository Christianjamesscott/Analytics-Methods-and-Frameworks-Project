from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw" / "uci_bank_marketing"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
OUTPUTS_DIR = ROOT_DIR / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGURES_DIR = OUTPUTS_DIR / "figures"
ARTIFACTS_DIR = OUTPUTS_DIR / "artifacts"

DEFAULT_DATASET_NAME = "bank"
TARGET_COLUMN = "y"
POSITIVE_TARGET_VALUE = "yes"
TOP_K_SHARE = 0.20
SCENARIO_CAPACITIES = (0.10, 0.20, 0.30)
TEST_SIZE = 0.20
RANDOM_STATE = 42

PROACTIVE_EXCLUDED_COLUMNS = [
    "contact",
    "day",
    "month",
    "duration",
    "campaign",
]

FEATURE_EXCLUSION_NOTES = {
    "contact": "Current-campaign contact method is a campaign-execution choice rather than a stable pre-contact customer attribute.",
    "day": "Last contact day in the current campaign is not available when prioritizing customers before outreach.",
    "month": "Current-campaign contact month is scheduling context, not a stable customer signal for early prioritization.",
    "duration": "Last contact duration is observed after contact and is explicit leakage for proactive prioritization.",
    "campaign": "Current-campaign contact count includes the last contact and is not known at the start of prioritization.",
}

TARGET_DEFINITION_NOTE = (
    "The target variable y is treated as a proxy for whether a customer is a strong "
    "candidate for proactive outreach, with 'yes' mapped to 1 and 'no' mapped to 0."
)

MODEL_SELECTION_RULE = (
    "Prefer the model with the highest precision in the top 20%, then break ties with "
    "top-20% recall and PR AUC."
)

DATASET_PATHS = {
    "bank": RAW_DATA_DIR / "bank" / "bank-full.csv",
    "bank_additional": (
        RAW_DATA_DIR
        / "bank-additional"
        / "bank-additional"
        / "bank-additional-full.csv"
    ),
}


def ensure_runtime_directories() -> None:
    for path in (PROCESSED_DATA_DIR, NOTEBOOKS_DIR, TABLES_DIR, FIGURES_DIR, ARTIFACTS_DIR):
        path.mkdir(parents=True, exist_ok=True)
