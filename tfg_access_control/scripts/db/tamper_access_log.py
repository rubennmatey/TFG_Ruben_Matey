from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.db.database import get_connection


def main():
    log_id = int(input("Introduce el id del log a modificar: "))
    new_reason = input("Nuevo reason: ").strip()

    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE access_logs
            SET reason = ?
            WHERE id = ?
            """,
            (new_reason, log_id)
        )
        conn.commit()
        print(f"Log {log_id} modificado correctamente.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()