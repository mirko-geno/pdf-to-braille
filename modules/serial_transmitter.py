import serial
import time

# Configuración del puerto serie
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Cambia 9600 por la velocidad adecuada

try:
    while True:
        ser.write(b'25')
        print("Dato enviado")
        time.sleep(1)

except KeyboardInterrupt:
    print("Programa terminado")

finally:
    ser.close()
