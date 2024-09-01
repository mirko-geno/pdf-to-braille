from machine import Pin
from time import sleep
import micropython
import select
import sys

led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)

micropython.kbd_intr(-1)

while flash_button.value():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:  # Only reads if theres something in the port
        byte = sys.stdin.buffer.read(1)  # Reads a byte from the serial port
        # print(f'Byte received: {byte}')
        
        if byte == b'\x98':
            led.value(not led.value())
    sleep(0.1)



# Configuración de pines para LEDs (asumiendo que están conectados a los pines 0-7)
led_pins = [Pin(i, Pin.OUT) for i in range(8)]

# Dato recibido (8 bits)
data = 0b10011000

# Procesamiento de cada bit para controlar los LEDs
for i in range(8):
    led_state = (data >> i) & 1  # Desplaza el bit i hacia la derecha y extrae el bit menos significativo
    led_pins[i].value(led_state)  # Establece el estado del LED basado en el bit correspondiente
