import time
import threading

from app.nfc.NFCReader import NFCReader
from app.core.access_controller import check_access
from app.ble.BLEServer import BLEServer
from app.services.enrollment_service import EnrollmentService


class AccessControlSystem:
    def __init__(self):
        self.reader = NFCReader()
        self.enrollment_service = EnrollmentService()
        self.ble = BLEServer(enrollment_service=self.enrollment_service)

    def start_ble(self):
        ble_thread = threading.Thread(target=self.ble.start, daemon=True)
        ble_thread.start()

    def run(self):
        self.start_ble()

        print("Sistema principal iniciado. Esperando tarjetas...")

        while True:
            uid = self.reader.read_uid()

            if uid:
                print(f"\nTarjeta detectada: {uid}")

                enroll_result = self.enrollment_service.handle_nfc_for_enrollment(uid)
                if enroll_result is not None:
                    print(f"[ENROLL] {enroll_result}")
                    self.ble.update_value(enroll_result)
                    time.sleep(2)
                    continue

                result = check_access(uid)
                print(result)

                message = f"{result['result']}:{uid}"
                self.ble.update_value(message)

                time.sleep(2)