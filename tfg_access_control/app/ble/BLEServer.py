from bluezero import peripheral
from app.ble.command_handler import handle_command

ADAPTER_ADDRESS = "2C:CF:67:E5:C9:88"

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
LAST_EVENT_UUID = "12345678-1234-5678-1234-56789abcdef1"
COMMAND_UUID = "12345678-1234-5678-1234-56789abcdef2"
RESPONSE_UUID = "12345678-1234-5678-1234-56789abcdef3"


class BLEServer:
    def __init__(self, enrollment_service=None):
        self.current_event = "INIT"
        self.current_response = "NO_RESPONSE"
        self.enrollment_service = enrollment_service

        self.peripheral = peripheral.Peripheral(
            adapter_address=ADAPTER_ADDRESS,
            local_name="TFG_ACCESS"
        )

        self.peripheral.add_service(
            srv_id=1,
            uuid=SERVICE_UUID,
            primary=True
        )

        self.peripheral.add_characteristic(
            srv_id=1,
            chr_id=1,
            uuid=LAST_EVENT_UUID,
            value=[],
            notifying=False,
            flags=["read"],
            read_callback=self.read_last_event
        )

        self.peripheral.add_characteristic(
            srv_id=1,
            chr_id=2,
            uuid=COMMAND_UUID,
            value=[],
            notifying=False,
            flags=["write"],
            write_callback=self.write_command
        )

        self.peripheral.add_characteristic(
            srv_id=1,
            chr_id=3,
            uuid=RESPONSE_UUID,
            value=[],
            notifying=False,
            flags=["read"],
            read_callback=self.read_response
        )

    def read_last_event(self):
        return list(self.current_event.encode("utf-8"))

    def update_value(self, new_value: str):
        self.current_event = new_value
        print(f"[BLE] LAST_EVENT actualizado a: {self.current_event}")

    def write_command(self, value, options):
        try:
            command = bytes(value).decode("utf-8").strip()
        except Exception:
            command = ""

        print(f"[BLE] Comando recibido: {command}")
        self.current_response = handle_command(command, self.enrollment_service)
        print(f"[BLE] Respuesta generada: {self.current_response}")

    def read_response(self):
        return list(self.current_response.encode("utf-8"))

    def start(self):
        print("BLE iniciado")
        self.peripheral.publish()