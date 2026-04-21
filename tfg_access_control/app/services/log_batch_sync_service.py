from app.db.log_batches import (
    list_pending_log_batches,
    mark_log_batch_as_synced,
)
from app.blockchain.log_batch_chain import send_log_batch_to_blockchain

# Sync 1 batch with blockchain
def sync_one_log_batch():
    pending = list_pending_log_batches()

    if not pending:
        return {"synced": 0, "message": "No hay lotes pendientes"}

    batch = pending[0]

    tx_hash, receipt = send_log_batch_to_blockchain(
        batch["batch_hash"],
        batch["created_at"]
    )

    mark_log_batch_as_synced(batch["id"], tx_hash)

    return {
        "synced": 1,
        "batch_id": batch["id"],
        "tx_hash": tx_hash,
        "block": receipt.blockNumber
    }

# Sync all batches with blockchain
def sync_all_log_batches():
    pending_batches = list_pending_log_batches()

    if not pending_batches:
        return {
            "synced": 0,
            "failed": 0,
            "message": "No hay lotes pendientes"
        }

    synced_count = 0
    failed_count = 0

    for batch in pending_batches:
        try:
            tx_hash, receipt = send_log_batch_to_blockchain(
                batch["batch_hash"],
                batch["created_at"]
            )

            mark_log_batch_as_synced(batch["id"], tx_hash)
            synced_count += 1

        except Exception as e:
            print(f"[SYNC_BATCH] Error sincronizando lote {batch['id']}: {e}")
            failed_count += 1

    return {
        "synced": synced_count,
        "failed": failed_count
    }