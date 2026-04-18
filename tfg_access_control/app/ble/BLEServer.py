from bluezero import peripheral

ADAPTER_ADDRESS = "2C:CF:67:E5:C9:88"

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"


class BLEServer:
    def __init__(self):
        self.value = b"INIT"

        self.peripheral = peripheral.Peripheral(
            adapter_address=ADAPTER_ADDRESS,
            local_name="TFG_ACCESS"
        )

        # Servicio
        self.peripheral.add_service(
            srv_id=1,
            uuid=SERVICE_UUID,
            primary=True
        )

        # Caracteristica
        self.peripheral.add_characteristic(
            srv_id=1,
            chr_id=1,
            uuid=CHAR_UUID,
            value=self.value,
            notifying=True,
            flags=["read", "notify"]
        )

        self.peripheral.add_advertising(
            local_name="TFG_ACCESS",
            service_uuid=SERVICE_UUID
        )

    def update_value(self, new_value: str):
        self.value = new_value.encode("utf-8")
        self.peripheral.update_characteristic_value(1, 1, self.value)

    def start(self):
        print("BLE iniciado")
        self.peripheral.publish()