import hashlib

# Generate a hash with a list of logs
def build_logs_batch_hash(log_rows):
    serialized_logs = []

    for row in log_rows:
        serialized_logs.append(
            f"{row['id']}|{row['uid']}|{row['result']}|{row['reason']}|{row['timestamp']}"
        )

    batch_payload = "||".join(serialized_logs)
    return hashlib.sha256(batch_payload.encode("utf-8")).hexdigest()