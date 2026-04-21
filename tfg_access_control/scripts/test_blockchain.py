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
    pending = list_pending_admin_actions()

    if not pending:
        print("No hay acciones pendientes.")
        return

    action = pending[0]

    print("Enviando acción a blockchain:")
    print(dict(action))

    tx_hash, receipt = send_admin_action_to_blockchain(
        action["action_type"],
        action["target_uid"],
        action["timestamp"]
    )

    mark_admin_action_as_synced(action["id"], tx_hash)

    print(f"Acción sincronizada correctamente.")
    print(f"tx_hash: {tx_hash}")
    print(f"blockNumber: {receipt.blockNumber}")


if __name__ == "__main__":
    main()