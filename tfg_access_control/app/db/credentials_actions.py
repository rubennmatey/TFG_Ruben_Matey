from datetime import datetime
from app.db.database import get_connection

# Function that creates a row on the table "credentials"
def create_credential(uid, alias, role = "user", active = 1):
    time = datetime.utcnow().isoformat()

    conn = get_connection()

    try:
        conn.execute("INSERT INTO credentials (uid, alias, role, active, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)", (uid, alias, role, active, time, time))
        conn.commit()
    finally:
        conn.close()
    
# Returns the credentials of an user from the uid
def get_credential_by_uid(uid):
    conn = get_connection()
    
    try:
        row = conn.execute("SELECT * FROM credentials WHERE uid = ?", (uid,)).fetchone()
        return row
    finally: 
        conn.close()

# Returns all the information from the table "credentials"
def list_credentials():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM credentials ORDER BY id").fetchall()
        return rows
    finally:
        conn.close()

# Returns a simplified list of credentials with uid, alias and active status
def list_credentials_as_rows():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT uid, alias, active FROM credentials ORDER BY id"
        ).fetchall()
        return rows
    finally:
        conn.close()

# Update the status of a card
def update_credential_status(uid, active):
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            UPDATE credentials
            SET active = ?, updated_at = datetime('now')
            WHERE uid = ?
            """,
            (active, uid)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

# Returns all the info form a card
def get_credential_summary(uid):
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT uid, alias, role, active
            FROM credentials
            WHERE uid = ?
            """,
            (uid,)
        ).fetchone()
        return row
    finally:
        conn.close()

# Checks that a credential exists
def credential_exists(uid):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT 1 FROM credentials WHERE uid = ?",
            (uid,)
        ).fetchone()
        return row is not None
    finally:
        conn.close()

