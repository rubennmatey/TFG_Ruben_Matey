import board
import busio
from adafruit_pn532.i2c import PN532_I2C


class NFCReader:

    # Initialize the I2C bus
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)

        self.pn532 = PN532_I2C(i2c, debug = False)

        self.pn532.SAM_configuration()

        print("Esperando tarjeta NFC...\n")

    # Reads the information from de I2C Bus
    def read_uid(self):
        uid = self.pn532.read_passive_target(timeout = 0.5)

        if uid is None:
            return None
        
        # Convert to string
        uid_str = ''.join([format(i, '02x') for i in uid])
        return uid_str