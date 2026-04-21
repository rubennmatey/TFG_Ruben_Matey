from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.db.admin_actions import (
    list_pending_admin_actions,
    mark_admin_action_as_synced,
)
from app.blockchain.admin_chain_service import send_admin_action_to_blockchain


def main():
    pending_actions = list_pending_admin_actions()

    if not pending_actions:
        print("No hay acciones pendientes de sincronizar.")
        return

    print(f"Acciones pendientes encontradas: {len(pending_actions)}")

    synced_count = 0
    failed_count = 0

    for action in pending_actions:
        try:
            print("\nSincronizando acción:")
            print(dict(action))

            tx_hash, receipt = send_admin_action_to_blockchain(
                action["action_type"],
                action["target_uid"],
                action["timestamp"]
            )

            mark_admin_action_as_synced(action["id"], tx_hash)

            print("Acción sincronizada correctamente")
            print(f"tx_hash: {tx_hash}")
            print(f"blockNumber: {receipt.blockNumber}")

            synced_count += 1

        except Exception as e:
            print(f"Error al sincronizar la acción id={action['id']}: {e}")
            failed_count += 1

    print("\n--- RESUMEN ---")
    print(f"Sincronizadas correctamente: {synced_count}")
    print(f"Fallidas: {failed_count}")


if __name__ == "__main__":
    main()