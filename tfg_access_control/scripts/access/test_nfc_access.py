from pathlib import Path
import sys
import time
import threading

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.nfc.NFCReader import NFCReader
from app.core.access_controller import check_access
from app.ble.BLEServer import BLEServer
from app.services.enrollment_service import EnrollmentService


def main():
    reader = NFCReader()
    enrollment_service = EnrollmentService()
    ble = BLEServer(enrollment_service=enrollment_service)

    ble_thread = threading.Thread(target=ble.start, daemon=True)
    ble_thread.start()

    print("Sistema iniciado. Esperando tarjetas...")

    while True:
        uid = reader.read_uid()

        if uid:
            print(f"\nTarjeta detectada: {uid}")

            enroll_result = enrollment_service.handle_nfc_for_enrollment(uid)
            if enroll_result is not None:
                print(f"[ENROLL] {enroll_result}")
                ble.update_value(enroll_result)
                time.sleep(2)
                continue

            result = check_access(uid)
            print(result)

            message = f"{result['result']}:{uid}"
            ble.update_value(message)

            time.sleep(2)


if __name__ == "__main__":
    main()