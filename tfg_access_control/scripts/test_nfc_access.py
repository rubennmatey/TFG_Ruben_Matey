from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.nfc.NFCReader import NFCReader
from app.core.access_controller import check_access
from app.ble.BLEServer import BLEServer


def main():
    reader = NFCReader()
    ble = BLEServer()
    ble.start()

    while True:
        uid = reader.read_uid()

        if uid:
            print(f"\nTarjeta detectada: {uid}")

            result = check_access(uid)
            print(result)

            message = f"{result['result']}:{uid}"
            ble.update_value(message)

            time.sleep(2)


if __name__ == "__main__":
    main()