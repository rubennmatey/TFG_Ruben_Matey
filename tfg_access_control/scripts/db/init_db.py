from pathlib import Path
import sys

# Añade la raiz del proyecto al path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from app.config import DATA_DIR, DB_PATH, SCHEMA_PATH
from app.db.database import get_connection


def init_database():
    DATA_DIR.mkdir(exist_ok=True)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print(f"Base de datos creada correctamente en: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()