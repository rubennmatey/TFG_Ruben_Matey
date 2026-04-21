from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.log_batch_verification_service import verify_log_batch_integrity


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/blockchain/verify_log_batch_integrity.py <batch_id>")
        return

    batch_id = int(sys.argv[1])

    result = verify_log_batch_integrity(batch_id)

    print("\n--- RESULTADO VERIFICACIÓN ---")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()