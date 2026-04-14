# File that contains the configuration of the project

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "access_control.db"
SCHEMA_PATH = BASE_DIR / "app" / "db" / "migrations" / "init_schema.sql"