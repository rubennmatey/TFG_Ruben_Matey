from bluezero import peripheral, async_tools

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
            flags=["read", "notify"],
            read_callback=self.read_value,
            write_callback=None,
            notify_callback=self.notify_callback
        )

    def read_value(self):
        print(f"[BLE] Read solicitado. Valor actual: {self.current_value}")
        return list(self.current_value.encode("utf-8"))

    def update_value(self, new_value: str):
        self.current_value = new_value
        print(f"[BLE] Valor actualizado a: {self.current_value}")

    def _notify_update(self, characteristic):
        print(f"[BLE] Enviando notify con valor: {self.current_value}")
        characteristic.set_value(list(self.current_value.encode("utf-8")))
        return characteristic.is_notifying

    def notify_callback(self, notifying, characteristic):
        print(f"[BLE] notify_callback llamado. notifying={notifying}")
        if notifying:
            async_tools.add_timer_seconds(1, self._notify_update, characteristic)

    def start(self):
        print("BLE iniciado")
        self.peripheral.publish()