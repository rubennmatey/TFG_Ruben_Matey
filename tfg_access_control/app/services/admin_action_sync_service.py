from app.db.admin_actions import (
    list_pending_admin_actions,
    mark_admin_action_as_synced,
)
from app.blockchain.admin_chain_service import send_admin_action_to_blockchain

# Tries to sync with blockchain 1 pending actions
def sync_one_pending_admin_action():
    pending = list_pending_admin_actions()

    if not pending:
        return {"synced": 0, "message": "No hay acciones admin pendientes"}

    action = pending[0]

    tx_hash, receipt = send_admin_action_to_blockchain(
        action["action_type"],
        action["target_uid"],
        action["timestamp"]
    )

    mark_admin_action_as_synced(action["id"], tx_hash)

    return {
        "synced": 1,
        "action_id": action["id"],
        "tx_hash": tx_hash,
        "block": receipt.blockNumber
    }

## Tries to sync with blockchain all pending actions
def sync_all_pending_admin_actions():
    pending_actions = list_pending_admin_actions()

    if not pending_actions:
        return {
            "synced": 0,
            "failed": 0,
            "message": "No hay acciones admin pendientes"
        }

    synced_count = 0
    failed_count = 0

    for action in pending_actions:
        try:
            tx_hash, receipt = send_admin_action_to_blockchain(
                action["action_type"],
                action["target_uid"],
                action["timestamp"]
            )

            mark_admin_action_as_synced(action["id"], tx_hash)
            synced_count += 1

        except Exception as e:
            print(f"[SYNC_ADMIN] Error sincronizando acción {action['id']}: {e}")
            failed_count += 1

    return {
        "synced": synced_count,
        "failed": failed_count
    }