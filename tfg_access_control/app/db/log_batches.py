from datetime import datetime
from app.db.database import get_connection

# Inserts new batch
def create_log_batch(batch_hash):
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO log_batches (batch_hash, created_at, synced_to_blockchain, tx_hash)
            VALUES (?, ?, 0, NULL)
            """,
            (batch_hash, now)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

# Lists all the batches by id
def list_log_batches():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM log_batches ORDER BY id DESC"
        ).fetchall()
        return rows
    finally:
        conn.close()

# Lists all batches not linked with the blockchain
def list_pending_log_batches():
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT * FROM log_batches
            WHERE synced_to_blockchain = 0
            ORDER BY id ASC
            """
        ).fetchall()
        return rows
    finally:
        conn.close()

# Link batch with blockchain
def mark_log_batch_as_synced(batch_id, tx_hash):
    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE log_batches
            SET synced_to_blockchain = 1,
                tx_hash = ?
            WHERE id = ?
            """,
            (tx_hash, batch_id)
        )
        conn.commit()
    finally:
        conn.close()


# Returns a log batch record by its local database ID
def get_log_batch_by_id(batch_id):
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT * FROM log_batches
            WHERE id = ?
            """,
            (batch_id,)
        ).fetchone()
        return row
    finally:
        conn.close()