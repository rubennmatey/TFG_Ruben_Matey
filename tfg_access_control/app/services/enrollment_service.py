from app.db.credentials_actions import create_credential, credential_exists
from app.db.admin_actions import create_admin_action
from app.constants import (
    BLE_RESPONSE_ENROLL_MODE_ON,
    BLE_RESPONSE_ENROLL_MODE_OFF,
    BLE_RESPONSE_NONE,
)


class EnrollmentService:
    def __init__(self):
        self.enroll_mode = False
        self.last_enrolled_uid = BLE_RESPONSE_NONE

    def start_enroll(self):
        self.enroll_mode = True
        return BLE_RESPONSE_ENROLL_MODE_ON

    def stop_enroll(self):
        self.enroll_mode = False
        return BLE_RESPONSE_ENROLL_MODE_OFF

    def get_last_enroll(self):
        return self.last_enrolled_uid

    def is_enroll_mode_active(self):
        return self.enroll_mode

    def handle_nfc_for_enrollment(self, uid):
        if not self.enroll_mode:
            return None

        if credential_exists(uid):
            self.enroll_mode = False
            self.last_enrolled_uid = f"ALREADY_EXISTS:{uid}"
            return self.last_enrolled_uid

        alias = f"NFC_{uid}"

        create_credential(
            uid=uid,
            alias=alias,
            role="user",
            active=1
        )

        create_admin_action(
            action_type="ENROLL_UID",
            target_uid=uid
        )

        try:
            result = send_credential_event_to_blockchain(
                uid=uid,
                action_type="REGISTER",
                role="user",
                active=True
            )
            print(f"[CREDENTIAL_CHAIN] REGISTER sincronizado: {result}")
        except Exception as e:
            print(f"[CREDENTIAL_CHAIN] Error registrando credential REGISTER: {e}")

        self.enroll_mode = False
        self.last_enrolled_uid = f"ENROLLED:{uid}"

        return self.last_enrolled_uid