from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.db.credentials_actions import list_credentials
from app.db.access_logs_actions import list_access_logs
from app.db.admin_actions import list_admin_actions
from app.db.log_batches import list_log_batches


def print_section(title, rows):
    print(f"\n=== {title} ===")
    if not rows:
        print("Sin datos")
        return
    for row in rows:
        print(dict(row))


def main():
    print_section("CREDENTIALS", list_credentials())
    print_section("ACCESS_LOGS", list_access_logs())
    print_section("ADMIN_ACTIONS", list_admin_actions())
    print_section("LOG_BATCHES", list_log_batches())


if __name__ == "__main__":
    main()