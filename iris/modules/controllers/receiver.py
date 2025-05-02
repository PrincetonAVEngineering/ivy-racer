import time
import serial

class ArduinoReceiver:
    def __init__(self, port: str, baud_rate: int = 9600):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            #self.serial_connection.setDTR(False)  # Prevent auto-reset
            time.sleep(1)
            print(f"Connected to Arduino on {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect to {self.port}: {e}")

    def receive_data(self):
        while True:
            if self.serial_connection and self.serial_connection.is_open:
                try:
                    if self.serial_connection.in_waiting:
                        data = self.serial_connection.read(1)  # Read a single byte
                        if data:
                            bit_string = format(ord(data), '08b')
                            print(f'Received data: {bit_string}')
                except Exception as e:
                    print(f"Failed to receive data: {e}")
            time.sleep(0.1)

def main():
    receiver = ArduinoReceiver('/dev/tty.usbmodem1101')
    receiver.connect()
    receiver.receive_data()  # This will block indefinitely and keep receiving

if __name__ == "__main__":
    main()
