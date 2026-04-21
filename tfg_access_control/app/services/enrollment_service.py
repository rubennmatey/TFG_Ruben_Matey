from app.db.credentials_actions import create_credential, credential_exists
from app.db.admin_actions import create_admin_action


class EnrollmentService:
    def __init__(self):
        self.enroll_mode = False
        self.last_enrolled_uid = "NONE"

    def start_enroll(self):
        self.enroll_mode = True
        return "ENROLL_MODE_ON"

    def stop_enroll(self):
        self.enroll_mode = False
        return "ENROLL_MODE_OFF"

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
        create_credential(uid, alias, role="user", active=1)
        create_admin_action("ENROLL_UID", uid)

        self.enroll_mode = False
        self.last_enrolled_uid = f"ENROLLED:{uid}"
        return self.last_enrolled_uid