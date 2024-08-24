import serial
import time

# Configuración del puerto serial
ser = serial.Serial('/dev/ttyUSB0', 115200) 
time.sleep(2)  # Espera a que se establezca la conexión

try:
    while True:
        ser.write(b'TOGGLE_LED\n')  # Envía el mensaje al ESP8266
        time.sleep(2)  # Envía un mensaje cada 2 segundos
        print('sent')
except KeyboardInterrupt:
    ser.close()  # Cierra el puerto serial al finalizar
    print('finishing...')

