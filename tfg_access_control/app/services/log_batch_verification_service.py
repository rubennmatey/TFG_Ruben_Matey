from app.db.log_batches import get_log_batch_by_id
from app.db.access_logs_actions import list_logs_by_batch_id
from app.blockchain.hashing import build_logs_batch_hash
from app.blockchain.log_batch_query_service import get_log_batch_from_blockchain


def verify_log_batch_integrity(batch_id):
    local_batch = get_log_batch_by_id(batch_id)
    if local_batch is None:
        return {
            "ok": False,
            "error": "LOCAL_BATCH_NOT_FOUND"
        }

    logs = list_logs_by_batch_id(batch_id)
    if not logs:
        return {
            "ok": False,
            "error": "NO_LOGS_FOR_BATCH"
        }

    recalculated_hash = build_logs_batch_hash(logs)

    blockchain_index = batch_id - 1 # -1 because on SQLite indexes start on 1
    blockchain_batch = get_log_batch_from_blockchain(blockchain_index)

    local_stored_hash = local_batch["batch_hash"]
    blockchain_hash = blockchain_batch["batch_hash"]

    return {
        "ok": recalculated_hash == blockchain_hash,
        "batch_id": batch_id,
        "local_stored_hash": local_stored_hash,
        "recalculated_hash": recalculated_hash,
        "blockchain_hash": blockchain_hash,
        "logs_count": len(logs),
    }