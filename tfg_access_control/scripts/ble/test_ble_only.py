from bluezero import peripheral

ADAPTER_ADDRESS = "2C:CF:67:E5:C9:88"

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"


def read_value():
    print("[BLE] Read solicitado")
    return list("HELLO".encode("utf-8"))


ble = peripheral.Peripheral(
    adapter_address=ADAPTER_ADDRESS,
    local_name="TFG_ACCESS"
)

ble.add_service(
    srv_id=1,
    uuid=SERVICE_UUID,
    primary=True
)

ble.add_characteristic(
    srv_id=1,
    chr_id=1,
    uuid=CHAR_UUID,
    value=[],
    notifying=False,
    flags=["read"],
    read_callback=read_value
)

print("BLE mï¿½nimo iniciado")
ble.publish()