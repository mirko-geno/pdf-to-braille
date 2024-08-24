import machine
import time
import sys

led = machine.Pin(2, machine.Pin.OUT)  # Configura el pin GPIO2 como salida (LED integrado)
led.value(1)  # Apaga el LED (los LED suelen estar activos en bajo en el ESP8266)

while True:
    if sys.stdin.read() == 'TOGGLE_LED\n':  # Lee el mensaje recibido
        led.value(not led.value())  # Alterna el estado del LED
    time.sleep(0.0001)  # Pequeña pausa para evitar saturación de la CPU
