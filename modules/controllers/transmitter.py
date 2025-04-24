import time
import serial

class ArduinoController:
    """
    A class to manage communication with a connected Arduino device.
    This class sends angle and throttle values to the Arduino.
    """



    #ALEXEI PROTOCOL 
    
    #a1a2b1c2c3c4c5    d1d2e1e2e3e4e5e6
    
    # 2 bytes
    
    #a1a2 -> 00 (angle)
    #b1 -> direction of angle (0 for clockwise 1 for counter clockwise)
    #c2c3c4c5 -> magnitude of angle
    
    #d1d2 -> 01 (throttle)
    #e1e2e3e4e5e6 -> (throttle magnitude)
    
    # (technically a 10 bit string is sent since UART automatically adds framing bits 
    # before and after our bytestring, but it also automatically decodes on the receiving side)
    
    


    def __init__(self, port: str, baud_rate: int = 9600):
        """
        Initialize the ArduinoController with the specified serial port and baud rate.
        
        :param port: The serial port to which the Arduino is connected (e.g., 'COM3', '/dev/ttyUSB0').
        :param baud_rate: The baud rate for serial communication. Default is 9600.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.angle = 0  # Angle value to send to the Arduino
        self.angle_direction = 0 #direction of angle
        self.throttle = 0  # Throttle value to send to the Arduino
        self.serial_connection = None  # Placeholder for the serial connection object

    def connect(self):
        
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            if self.serial_connection.is_open:
                print(f"Connected to Arduino on {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect to {self.port}: {e}")

    def disconnect(self):
        
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial connection closed.")
        else:
            print("Serial connection was not open.")


    #Set angle (1 byte)
    def set_angle(self, angle: int):
        
        if angle > 255 or angle < -255:
            print('Angle input should be [0,255] (one unsigned byte)')
        
        self.angle = angle

    #Set Throttle (1 byte)
    def set_throttle(self, throttle: int):
        
        if throttle > 255 or throttle < 0:
            print('Throttle input value should be [0,255] (one unsigned byte)')
            return        
        
        self.throttle = throttle
    
    
    def set_angle_direction(self, direction: int):
        
        if direction != 1 and direction != 0:
            print('Direction can only be 0 or 1')
            return    
        
        self.angle_direction = direction  
        



    def send_data(self):
        """
        Send the current angle and throttle values to the Arduino.
        """
        # TODO: Implement the logic to format and send data over the serial connection.
        # Create a communication protocol for this.
        # 1 byte for throttle 1 byte for angle 1 byte direction
        # 
        # GPT: Your computer's UART hardware (or USB-to-Serial adapter) automatically adds the 
        # framing bits — just like the Arduino does on its end.
        
        #for testing
        first_byte = (self.angle_direction << 5) | (self.angle & 0x1F)
        #second_byte = (0x01 << 6) | (self.throttle & 0x3F)
        
        # 1 bit + 7 bits of 0s
        message = bytes([first_byte])
        
        bit_string = ' '.join(format(byte, '08b') for byte in message)
        print('sending:', bit_string)
        
        
        if self.serial_connection and self.serial_connection.is_open:
           
           self.serial_connection.write(message)


    def receive_data(self):
        
        if self.serial_connection and self.serial_connection.is_open:
            print('inside here')
            time.sleep(1)
            try:
                if self.serial_connection.in_waiting > 0:
                    print('inside double here')
                    data = self.serial_connection.read(1)  # Read a single byte
                    if data:
                        print(f"Received byte from Arduino: {data} ({format(ord(data), '08b')})")
                        return data
            except Exception as e:
                print(f"Failed to receive data from Arduino: {e}")
                return None
        else:
            print("Cannot receive data. No active serial connection.")
            return None
        
    
    

def test_arduino_controller():
    # Adjust this to your actual port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux/Mac)
    port = '/dev/tty.usbmodem11301' # Replace with your real port

    arduino = ArduinoController(port)
    #arduino.connect()
    arduino.connect()
    
    arduino.set_angle(0)
    arduino.set_throttle(0)
    arduino.set_angle_direction(1)
    arduino.send_data()
    arduino.receive_data()
    #arduino.disconnect()
    # Optionally receive response
    time.sleep(1)

if __name__ == "__main__":
    test_arduino_controller()