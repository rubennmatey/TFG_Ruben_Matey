from bluezero import peripheral

ADAPTER_ADDRESS = "2C:CF:67:E5:C9:88"

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"


class BLEServer:
    def __init__(self):
        self.current_value = "INIT"

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
            uuid=CHAR_UUID,
            value=[],
            notifying=False,
            flags=["read"],
            read_callback=self.read_value
        )

    def read_value(self):
        print(f"[BLE] Read solicitado. Valor actual: {self.current_value}")
        return list(self.current_value.encode("utf-8"))

    def update_value(self, new_value: str):
        self.current_value = new_value
        print(f"[BLE] Valor actualizado a: {self.current_value}")

    def start(self):
        print("BLE iniciado")
        self.peripheral.publish()