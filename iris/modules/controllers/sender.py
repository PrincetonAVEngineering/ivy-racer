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
            try:
                # Ensure byte_data is an int 0-255
                if not isinstance(byte_data, int):
                    raise ValueError("byte_data must be an integer 0-255")
                byte_to_send = byte_data.to_bytes(1, byteorder='big')
                self.serial_connection.write(byte_to_send)
                bit_string = format(byte_data, '08b')
                # print(f'Sent data: {bit_string}')
            except Exception as e:
                print(f"comms fail: {e}")
                self.disconnect()
                time.sleep(0.1)
                self.connect()

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

    def disconnect(self):
        
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial connection closed.")
        else:
            print("Serial connection was not open.")

def main():
    sender = ArduinoSender('COM5')
    sender.connect()
    sender.interactive_input()

if __name__ == "__main__":
    main()
