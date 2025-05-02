import serial

class ArduinoController:
    """
    A class to manage communication with a connected Arduino device.
    This class sends angle and throttle values to the Arduino.
    """

    def __init__(self, port: str, baud_rate: int = 9600):
        """
        Initialize the ArduinoController with the specified serial port and baud rate.
        
        :param port: The serial port to which the Arduino is connected (e.g., 'COM3', '/dev/ttyUSB0').
        :param baud_rate: The baud rate for serial communication. Default is 9600.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.angle = 0  # Angle value to send to the Arduino
        self.throttle = 0  # Throttle value to send to the Arduino
        self.serial_connection = None  # Placeholder for the serial connection object
        self.direction = "R"

    def connect(self):
        """
        Establish a serial connection to the Arduino.
        """
        try:
            # Close any existing connection
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                
            # Add a small delay before reopening
            import time
            time.sleep(1)
                
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=1,
                write_timeout=1
            )
            
            # Wait for Arduino to reset
            time.sleep(2)
            
            print(f"Connected to Arduino on port {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino: {e}")
            print(f"Please verify that {self.port} is correct and no other program is using it.")
            self.serial_connection = None
        except Exception as e:
            print(f"Unexpected error while connecting to Arduino: {e}")
            self.serial_connection = None

    def disconnect(self):
        """
        Close the serial connection to the Arduino.
        """
        # TODO: Implement the logic to safely close the serial connection.
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
                print(f"Disconnected from Arduino on port {self.port}.")
            except Exception as e:
                print(f"Failed to disconnect from Arduino: {e}")
        else:
            print("No active connection to disconnect.")
        pass

    def set_angle(self, angle: int):
        """
        Update the angle value to be sent to the Arduino.
        
        :param angle: The new angle value.
        """
        self.angle = angle

    def set_throttle(self, throttle: int):
        """
        Update the throttle value to be sent to the Arduino.
        
        :param throttle: The new throttle value.
        """
        self.throttle = throttle

    def set_direction(self, direction: str):
        self.direction = direction[0]

    def send_data(self):
        """
        Send the current angle and throttle values to the Arduino.
        """
        # TODO: Implement the logic to format and send data over the serial connection.
        # Create a communication protocol for this.

        if self.serial_connection and self.serial_connection.is_open:
            try:
                # Communication protocol: Send data as "ANGLE:<angle>,DIR:<dir>\n"
                data = f"ANGLE:{self.angle},DIR:{self.direction}\n"
                self.serial_connection.write(data.encode('utf-8'))
                print(f"Sent data to Arduino: {data.strip()}")
            except Exception as e:
                print(f"Failed to send data to Arduino: {e}")
        else:
            print("Cannot send data. No active serial connection.")
        

    def receive_data(self):
        """
        Receive data from the Arduino (if necessary).
        """
        # TODO: Implement the logic to read and process data from the Arduino.
        if self.serial_connection and self.serial_connection.is_open:
            try:
                # Read a line of data from the Arduino
                data = self.serial_connection.readline().decode('utf-8').strip()
                if data:
                    print(f"Received data from Arduino: {data}")
                    return data
            except Exception as e:
                print(f"Failed to receive data from Arduino: {e}")
                return None
        else:
            print("Cannot receive data. No active serial connection.")
            return None

if __name__ == "__main__":
    # Example usage of the ArduinoController class
    port = "COM5"  # Replace with the actual port your Arduino is connected to
    baud_rate = 9600

    controller = ArduinoController(port, baud_rate)

    try:
        # Connect to the Arduino
        controller.connect()

        # Set angle and throttle values
        controller.set_angle(45)
        controller.set_direction("L")

        # Send data to the Arduino
        controller.send_data()

        # Optionally, receive data from the Arduino
        response = controller.receive_data()
        if response:
            print(f"Arduino response: {response}")

    finally:
        # Ensure the connection is closed properly
        controller.disconnect()