from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.log_batch_sync_service import sync_all_log_batches


def main():
    result = sync_all_log_batches()

    print("\n--- RESULTADO ---")
    print(result)


if __name__ == "__main__":
    main()