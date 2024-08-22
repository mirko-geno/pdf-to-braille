import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 9600)
print('banana')
   
# Send character 'S' to start the program
ser.write(b'S')

# Read line   
while True:
    print('banan2')
    bs = ser.readline()
    print(f'BS:{bs}')