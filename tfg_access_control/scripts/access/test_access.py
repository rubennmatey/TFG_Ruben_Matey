from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from app.core.access_controller import check_access
from app.db.access_logs_actions import list_access_logs

def main():
    uids = ["49724e06", "a31d1656", "ffffffff"]

    for uid in uids:
        result = check_access(uid)
        print(f"\nPrueba UID: {uid}")
        print(result)

    print("\nLogs de acceso:")
    for row in list_access_logs():
        print(dict(row))


if __name__ == "__main__":
    main()