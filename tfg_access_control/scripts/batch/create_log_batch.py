from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from app.services.batch_service import create_logs_batch


def main():
    batch_id, logs = create_logs_batch(batch_size=3)

    if batch_id is None:
        print("No hay suficientes logs sin agrupar para crear un lote.")
        return

    print(f"Lote creado correctamente. batch_id={batch_id}")
    print("Logs incluidos:")

    for row in logs:
        print(dict(row))


if __name__ == "__main__":
    main()