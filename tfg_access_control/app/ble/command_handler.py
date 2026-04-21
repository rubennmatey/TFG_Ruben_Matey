from app.db.access_logs_actions import get_last_access_log
from app.db.credentials_actions import (
    list_credentials_as_rows,
    get_credential_summary,
    update_credential_status,
)
from app.db.admin_actions import create_admin_action


def handle_command(command: str, enrollment_service=None) -> str:
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

    if command.startswith("GET_CREDENTIAL:"):
        uid = command.split(":", 1)[1].strip()
        row = get_credential_summary(uid)

        if row is None:
            return "CREDENTIAL_NOT_FOUND"

        return f"{row['uid']}:{row['alias']}:{row['role']}:{row['active']}"

    if command.startswith("DISABLE_UID:"):
        uid = command.split(":", 1)[1].strip()
        updated = update_credential_status(uid, 0)

        if updated == 0:
            return "CREDENTIAL_NOT_FOUND"

        create_admin_action("DISABLE_UID", uid)
        return f"UID_DISABLED:{uid}"

    if command.startswith("ENABLE_UID:"):
        uid = command.split(":", 1)[1].strip()
        updated = update_credential_status(uid, 1)

        if updated == 0:
            return "CREDENTIAL_NOT_FOUND"

        create_admin_action("ENABLE_UID", uid)
        return f"UID_ENABLED:{uid}"

    if command == "START_ENROLL":
        if enrollment_service is None:
            return "ENROLL_SERVICE_NOT_AVAILABLE"
        return enrollment_service.start_enroll()

    if command == "STOP_ENROLL":
        if enrollment_service is None:
            return "ENROLL_SERVICE_NOT_AVAILABLE"
        return enrollment_service.stop_enroll()

    if command == "GET_LAST_ENROLL":
        if enrollment_service is None:
            return "ENROLL_SERVICE_NOT_AVAILABLE"
        return enrollment_service.get_last_enroll()

    return "UNKNOWN_COMMAND"