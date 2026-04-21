from datetime import datetime
from app.db.database import get_connection

# Insert 
def create_admin_action(action_type, target_uid):
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO admin_actions (action_type, target_uid, timestamp, synced_to_blockchain, tx_hash)
            VALUES (?, ?, ?, 0, NULL)
            """,
            (action_type, target_uid, now)
        )
        conn.commit()
    finally:
        conn.close()

# Returns all the admin actions
def list_admin_actions():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM admin_actions ORDER BY id DESC"
        ).fetchall()
        return rows
    finally:
        conn.close()

# Returns all the pending actions not linked with blockchain
def list_pending_admin_actions():
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT * FROM admin_actions
            WHERE synced_to_blockchain = 0
            ORDER BY id ASC
            """
        ).fetchall()
        return rows
    finally:
        conn.close()


def mark_admin_action_as_synced(action_id, tx_hash):
    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE admin_actions
            SET synced_to_blockchain = 1,
                tx_hash = ?
            WHERE id = ?
            """,
            (tx_hash, action_id)
        )
        conn.commit()
    finally:
        conn.close()