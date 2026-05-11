from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.credential_verification_service import verify_credentials_against_blockchain


def main():
    results = verify_credentials_against_blockchain()

    print("\n--- VERIFICACIÓN DE CREDENCIALES CONTRA BLOCKCHAIN ---")

    if not results:
        print("No hay credenciales en SQLite.")
        return

    valid_count = 0
    invalid_count = 0

    for result in results:
        print("\nCredencial:")
        for key, value in result.items():
            print(f"  {key}: {value}")

        if result["status"] == "VALID":
            valid_count += 1
        else:
            invalid_count += 1

    print("\n--- RESUMEN ---")
    print(f"Credenciales válidas: {valid_count}")
    print(f"Credenciales sospechosas: {invalid_count}")

    if invalid_count == 0:
        print("Resultado global: OK")
    else:
        print("Resultado global: INCONSISTENCIAS DETECTADAS")


if __name__ == "__main__":
    main()