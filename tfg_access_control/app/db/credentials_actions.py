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

def list_credentials_as_rows():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT uid, alias, active FROM credentials ORDER BY id"
        ).fetchall()
        return rows
    finally:
        conn.close()


