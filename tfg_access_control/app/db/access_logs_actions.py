from datetime import datetime
from app.db.database import get_connection

# Function that creates a row on the table "access_logs"
def create_access_log(uid, result, reason):
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO access_logs (uid, result, reason, timestamp, batched, batch_id)
            VALUES (?, ?, ?, ?, 0, NULL)
            """,
            (uid, result, reason, now)
        )
        conn.commit()
    finally:
        conn.close()
    
# Returns all the logs 
def list_access_logs():
    conn = get_connection()

    try:
        rows = conn.execute("SELECT * FROM access_logs ORDER BY id DESC").fetchall()
        return rows
    finally:
        conn.close()

# Returns the last access log
def get_last_access_log():
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM access_logs ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return row
    finally:
        conn.close()

# Returns all the logs that are not linked with a batch
def list_unbatched_access_logs(limit=3):
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT * FROM access_logs
            WHERE batched = 0
            ORDER BY id ASC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()
        return rows
    finally:
        conn.close()

# Link logs to a batch
def mark_logs_as_batched(log_ids, batch_id):
    if not log_ids:
        return

    conn = get_connection()
    try:
        placeholders = ",".join(["?"] * len(log_ids))
        query = f"""
            UPDATE access_logs
            SET batched = 1,
                batch_id = ?
            WHERE id IN ({placeholders})
        """
        conn.execute(query, [batch_id] + log_ids)
        conn.commit()
    finally:
        conn.close()