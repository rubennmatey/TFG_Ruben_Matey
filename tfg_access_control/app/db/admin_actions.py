from datetime import datetime
from app.db.database import get_connection

# Insert 
def create_admin_action(action_type, target_uid):
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO admin_actions (action_type, target_uid, timestamp)
            VALUES (?, ?, ?)
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