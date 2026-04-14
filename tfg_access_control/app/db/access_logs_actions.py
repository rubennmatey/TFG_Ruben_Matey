from datetime import datetime
from app.db.database import get_connection

# Function that creates a row on the table "access_logs"
def create_access_log(uid, result, reason):
    time = datetime.utcnow().isoformat()

    conn = get_connection()
    try:
        conn.execute("INSERT INTO access_logs (uid, result, reason, timestamp) VALUES (?, ?, ?, ?)", (uid, result, reason, time))
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
