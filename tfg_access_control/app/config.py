# File that contains the configuration of the project

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "access_control.db"
SCHEMA_PATH = BASE_DIR / "app" / "db" / "migrations" / "init_schema.sql"

BLOCKCHAIN_RPC_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x5161f0bd5D9124597E1cd6E199703e3cFF613BD4"
CHAIN_ID = 1337

BLOCKCHAIN_ACCOUNT = "0x82c5D9bEB0F8AC33Fddaa3d5Fd3B308588671Fa4"
BLOCKCHAIN_PRIVATE_KEY = "0x14bb0b7717d3eb3dad864ae962c806af15593c140f28b6faf662885cb63ee341"