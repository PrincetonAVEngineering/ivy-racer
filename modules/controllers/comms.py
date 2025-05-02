import serial
import time

arduino = serial.Serial(port="COM5", baudrate=9600, timeout=0.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    data = arduino.readline()
    return data

while True:
    throttle = input("Enter Throttle: ")
    value = write_read(throttle)
    print(value)