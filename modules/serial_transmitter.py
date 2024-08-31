import serial
import time

# Configuración del puerto serie
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Cambia 9600 por la velocidad adecuada
data = b'Q'
ser.write(data)
print(f'Dato enviado {data}')

ser.close()
