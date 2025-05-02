import time
import serial

class ArduinoSender:
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

    def send_data(self, byte_data):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(byte_data)
            bit_string = format(ord(byte_data), '08b')
            print(f'Sent data: {bit_string}')

    def interactive_input(self):
        while True:
            user_input = input("Enter 8 bits (e.g., '01010101') to send to Arduino (or 'exit' to quit): ")
            
            if user_input.lower() == 'exit':
                print("Exiting sender module.")
                break

            if len(user_input) != 8 or not all(bit in '01' for bit in user_input):
                print("Invalid input. Please enter exactly 8 bits.")
                continue

            byte_data = int(user_input, 2).to_bytes(1, byteorder='big')
            self.send_data(byte_data)

def main():
    sender = ArduinoSender('COM5')
    sender.connect()
    sender.interactive_input()

if __name__ == "__main__":
    main()
