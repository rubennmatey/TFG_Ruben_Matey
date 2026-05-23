from app.db.credentials_actions import create_credential, credential_exists
from app.db.admin_actions import create_admin_action
from app.blockchain.credential_chain_service import register_credential_on_blockchain
from app.constants import (
    BLE_RESPONSE_ENROLL_MODE_ON,
    BLE_RESPONSE_ENROLL_MODE_OFF,
    BLE_RESPONSE_NONE,
)


class EnrollmentService:
    # Initializes the enrollment service with enroll mode disabled
    def __init__(self):
        self.enroll_mode = False
        self.last_enrolled_uid = BLE_RESPONSE_NONE

    # Activates enrollment mode so the next NFC scan registers a new credential
    def start_enroll(self):
        self.enroll_mode = True
        return BLE_RESPONSE_ENROLL_MODE_ON

    # Deactivates enrollment mode
    def stop_enroll(self):
        self.enroll_mode = False
        return BLE_RESPONSE_ENROLL_MODE_OFF

    # Returns the UID result of the last enrollment attempt
    def get_last_enroll(self):
        return self.last_enrolled_uid

    # Returns whether enrollment mode is currently active
    def is_enroll_mode_active(self):
        return self.enroll_mode

    # Handles a scanned NFC UID during enrollment mode and registers it if new
    def handle_nfc_for_enrollment(self, uid):
        if not self.enroll_mode:
            return None

        if credential_exists(uid):
            self.enroll_mode = False
            self.last_enrolled_uid = f"ALREADY_EXISTS:{uid}"
            return self.last_enrolled_uid

        alias = f"NFC_{uid}"
        role = "user"
        active = 1

        create_credential(
            uid=uid,
            alias=alias,
            role=role,
            active=active
        )

        create_admin_action(
            action_type="ENROLL_UID",
            target_uid=uid
        )

        try:
            result = register_credential_on_blockchain(
                uid=uid,
                alias=alias,
                role=role,
                active=bool(active)
            )
            print(f"[CREDENTIAL_CHAIN] Credencial registrada en blockchain: {result}")
        except Exception as e:
            print(f"[CREDENTIAL_CHAIN] Error registrando credencial en blockchain: {e}")

        self.enroll_mode = False
        self.last_enrolled_uid = f"ENROLLED:{uid}"

        return self.last_enrolled_uid