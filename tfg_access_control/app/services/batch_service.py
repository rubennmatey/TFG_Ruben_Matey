from app.db.access_logs_actions import (
    list_unbatched_access_logs,
    mark_logs_as_batched,
)
from app.db.log_batches import create_log_batch
from app.blockchain.hashing import build_logs_batch_hash


def create_logs_batch(batch_size=3):
    logs = list_unbatched_access_logs(limit=batch_size)

    if len(logs) < batch_size:
        return None, []

    batch_hash = build_logs_batch_hash(logs)
    batch_id = create_log_batch(batch_hash)

    log_ids = [row["id"] for row in logs]
    mark_logs_as_batched(log_ids, batch_id)

    return batch_id, logs