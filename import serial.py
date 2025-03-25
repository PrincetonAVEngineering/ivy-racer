import serial
import time

# Open the serial connection (update port name accordingly)
ser = serial.Serial('COM3', 9600)  # For Windows
time.sleep(2)  # Give the connection a moment to initialize
# ser = serial.Serial('/dev/ttyUSB0', 9600)  # For Linux/Mac
if:  
    ser.print("");
def read_array():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()  # Read a line and decode it
            if line:
                array = list(map(int, line.split(',')))  # Convert string to list of integers
                print("Received array:", array)
        except ValueError:
            print("Data error, skipping...")
        except KeyboardInterrupt:
            print("Exiting...")
            ser.close()
            break
        finally: 
            ser.close()
read_array()
