import machine
import time

# Configuración del puerto serie
uart = machine.UART(0, baudrate=9600)  # Usa UART0 con baudrate de 9600
led = machine.Pin(2, machine.Pin.OUT)  # El LED interno está en el pin GPIO 2 en el ESP8266

while True:
    if uart.any():  # Verifica si hay datos en el buffer serial
        uart.read(1)  # Lee 1 byte (el dato enviado)
        led.value(not led.value())  # Alterna el estado del LED
        print("Dato recibido, LED alternado")
        time.sleep(0.1)  # Añade un pequeño retraso para evitar posibles rebotes
