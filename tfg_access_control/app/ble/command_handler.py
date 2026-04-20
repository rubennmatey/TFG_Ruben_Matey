from app.db.access_logs_actions import get_last_access_log
from app.db.credentials_actions import list_credentials_as_rows


def handle_command(command: str) -> str:
    command = command.strip()

    if command == "PING":
        return "PONG"

    if command == "GET_LAST_LOG":
        row = get_last_access_log()
        if row is None:
            return "NO_LOGS"

        return f"{row['uid']}:{row['result']}:{row['reason']}:{row['timestamp']}"

    if command == "LIST_CREDENTIALS":
        rows = list_credentials_as_rows()
        if not rows:
            return "NO_CREDENTIALS"

        parts = []
        for row in rows:
            parts.append(f"{row['uid']}:{row['alias']}:{row['active']}")
        return "|".join(parts)

    return "UNKNOWN_COMMAND"