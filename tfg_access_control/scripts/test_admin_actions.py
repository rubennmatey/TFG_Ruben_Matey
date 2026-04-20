from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.db.admin_actions import list_admin_actions


def main():
    rows = list_admin_actions()

    if not rows:
        print("No hay acciones administrativas guardadas.")
        return

    for row in rows:
        print(dict(row))


if __name__ == "__main__":
    main()