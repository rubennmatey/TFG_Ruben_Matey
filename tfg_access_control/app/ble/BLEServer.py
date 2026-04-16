from bluezero import peripheral

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

class BLEServer:
    def __init__(self):
        self.value = b"INIT"

        self.peripheral = peripheral.Peripheral(
            adapter_addr = None,
            local_name = "TFG_ACCESS"
        )

        self.peripheral.add_service(
            srv_id = 1,
            uuid = SERVICE_UUID,
            primary = True
        )

        self.peripheral.add_characteristic(
            srv_id = 1,
            chr_id = 1,
            uuid = CHAR_UUID,
            value = self.value,
            notifying = True,
            flags = ["read", "notify"]
        )

        def update_value(self, new_value: str):
            self.value = new_value.encode("utf-8")
            self.peripheral.update_characteristic_value(1,1, self.value)

        def start(self):
            print("BLE iniciado")
        self.peripheral.publish()
