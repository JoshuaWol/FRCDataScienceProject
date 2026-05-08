import os


from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.environ['POSTGRESQL_PASSWORD']
DB_USERNAME = os.environ['POSTGRESQL_USERNAME']
DB_NAME = os.environ['POSTGRESQL_DB_FRCDATASCIENCE']
DB_HOST = '127.0.0.1'
DB_PORT = '5432'

START_YEAR = 2026
END_YEAR = 2010
CURR_YEAR = 2026


REPO_ROOT = Path(__file__).resolve().parent
JSON_DIR = REPO_ROOT / 'api' / 'json'
DISTRICT_JSON_DIR = JSON_DIR / 'districts_data'
EVENTS_JSON_DIR = JSON_DIR / 'events_data'
MATCHES_JSON_DIR = JSON_DIR / 'matches_data'
REFERENCE_JSON_DIR = JSON_DIR / 'reference_data'
SEASONS_JSON_DIR = JSON_DIR / 'seasons_data'
TEAMS_JSON_DIR = JSON_DIR / 'teams_data'


SCHEMA = "public"
if_exists = 'append'