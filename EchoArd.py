import serial
import time

# Adjust 'COM3' for Windows or '/dev/ttyUSB0' for Linux/Mac
ser = serial.Serial('COM3', 9600, timeout=1)  
time.sleep(2)  # Allow time for Arduino to initialize

def send_and_receive(data):
    ser.write((data + "\n").encode())  # Send data with newline
    time.sleep(0.1)  # Give Arduino time to process
    response = ser.readline().decode('utf-8').strip()  # Read response
    return response

try:
    while True:
        user_input = input("Enter a string to send (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response = send_and_receive(user_input)
        print("Arduino echoed:", response)
finally:
    ser.close()
