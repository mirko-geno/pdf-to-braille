import serial
import time

# Configuración del puerto serie
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Must use baudrate of 115200 to work

data = 0b10011000
data = data.to_bytes(1, 'big')  # bits to byte object

ser.write(data)
print(f'Dato enviado: {data}')

ser.close()
