from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
JSON_DIR = REPO_ROOT / 'api' / 'json'
DISTRICT_JSON_DIR = JSON_DIR / 'districts_data'
EVENTS_JSON_DIR = JSON_DIR / 'events_data'
MATCHES_JSON_DIR = JSON_DIR / 'matches_data'
REFERENCE_JSON_DIR = JSON_DIR / 'reference_data'
SEASONS_JSON_DIR = JSON_DIR / 'seasons_data'
TEAMS_JSON_DIR = JSON_DIR / 'teams_data'
PY_LOAD_DIR = REPO_ROOT / 'sql' / 'scripts' / 'load_files'
SQL_LOAD_DIR = REPO_ROOT / 'sql' / 'features' / 'load_files'
DATA_SCIENCE_DIR = REPO_ROOT / 'data_science'
EDA_DIR = DATA_SCIENCE_DIR / 'eda'