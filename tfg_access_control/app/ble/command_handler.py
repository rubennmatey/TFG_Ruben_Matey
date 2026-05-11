from app.db.access_logs_repository import get_last_access_log
from app.db.credentials_repository import (
    list_credentials_as_rows,
    get_credential_summary,
    update_credential_status,
)
from app.db.admin_actions_repository import create_admin_action
from app.blockchain.credential_chain_service import send_credential_event_to_blockchain
from app.constants import (
    BLE_RESPONSE_PONG,
    BLE_RESPONSE_UNKNOWN_COMMAND,
    BLE_RESPONSE_INVALID_ARGUMENTS,
    BLE_RESPONSE_NO_LOGS,
    BLE_RESPONSE_NO_CREDENTIALS,
    BLE_RESPONSE_CREDENTIAL_NOT_FOUND,
    BLE_RESPONSE_ENROLL_SERVICE_NOT_AVAILABLE,
)


def _extract_uid(command: str):
    parts = command.split(":", 1)

    if len(parts) != 2:
        return None

    uid = parts[1].strip()

    if not uid:
        return None

    return uid


def handle_command(command: str, enrollment_service=None) -> str:
    command = command.strip()

    if not command:
        return BLE_RESPONSE_UNKNOWN_COMMAND

    if command == "PING":
        return BLE_RESPONSE_PONG

    if command == "GET_LAST_LOG":
        row = get_last_access_log()

        if row is None:
            return BLE_RESPONSE_NO_LOGS

        return f"{row['uid']}:{row['result']}:{row['reason']}:{row['timestamp']}"

    if command == "LIST_CREDENTIALS":
        rows = list_credentials_as_rows()

        if not rows:
            return BLE_RESPONSE_NO_CREDENTIALS

        parts = []

        for row in rows:
            parts.append(f"{row['uid']}:{row['alias']}:{row['active']}")

        return "|".join(parts)

    if command.startswith("GET_CREDENTIAL:"):
        uid = _extract_uid(command)

        if uid is None:
            return BLE_RESPONSE_INVALID_ARGUMENTS

        row = get_credential_summary(uid)

        if row is None:
            return BLE_RESPONSE_CREDENTIAL_NOT_FOUND

        return f"{row['uid']}:{row['alias']}:{row['role']}:{row['active']}"

    if command.startswith("DISABLE_UID:"):
        uid = _extract_uid(command)

        if uid is None:
            return BLE_RESPONSE_INVALID_ARGUMENTS

        row = get_credential_summary(uid)

        if row is None:
            return BLE_RESPONSE_CREDENTIAL_NOT_FOUND

        updated = update_credential_status(uid, 0)

        if updated == 0:
            return BLE_RESPONSE_CREDENTIAL_NOT_FOUND

        create_admin_action(
            action_type="DISABLE_UID",
            target_uid=uid
        )

        try:
            result = send_credential_event_to_blockchain(
                uid=uid,
                action_type="DISABLE",
                role=row["role"],
                active=False
            )
            print(f"[CREDENTIAL_CHAIN] DISABLE sincronizado: {result}")
        except Exception as e:
            print(f"[CREDENTIAL_CHAIN] Error registrando credential DISABLE: {e}")

        return f"UID_DISABLED:{uid}"

    if command.startswith("ENABLE_UID:"):
        uid = _extract_uid(command)

        if uid is None:
            return BLE_RESPONSE_INVALID_ARGUMENTS

        row = get_credential_summary(uid)

        if row is None:
            return BLE_RESPONSE_CREDENTIAL_NOT_FOUND

        updated = update_credential_status(uid, 1)

        if updated == 0:
            return BLE_RESPONSE_CREDENTIAL_NOT_FOUND

        create_admin_action(
            action_type="ENABLE_UID",
            target_uid=uid
        )

        try:
            result = send_credential_event_to_blockchain(
                uid=uid,
                action_type="ENABLE",
                role=row["role"],
                active=True
            )
            print(f"[CREDENTIAL_CHAIN] ENABLE sincronizado: {result}")
        except Exception as e:
            print(f"[CREDENTIAL_CHAIN] Error registrando credential ENABLE: {e}")

        return f"UID_ENABLED:{uid}"

    if command == "START_ENROLL":
        if enrollment_service is None:
            return BLE_RESPONSE_ENROLL_SERVICE_NOT_AVAILABLE

        return enrollment_service.start_enroll()

    if command == "STOP_ENROLL":
        if enrollment_service is None:
            return BLE_RESPONSE_ENROLL_SERVICE_NOT_AVAILABLE

        return enrollment_service.stop_enroll()

    if command == "GET_LAST_ENROLL":
        if enrollment_service is None:
            return BLE_RESPONSE_ENROLL_SERVICE_NOT_AVAILABLE

        return enrollment_service.get_last_enroll()

    return BLE_RESPONSE_UNKNOWN_COMMAND