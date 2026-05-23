import sqlite3
from app.config import DB_PATH


# Returns an open SQLite connection with row factory enabled
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn