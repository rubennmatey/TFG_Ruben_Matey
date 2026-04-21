from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.db.log_batches import list_log_batches


def main():
    rows = list_log_batches()

    if not rows:
        print("No hay lotes creados.")
        return

    for row in rows:
        print(dict(row))


if __name__ == "__main__":
    main()