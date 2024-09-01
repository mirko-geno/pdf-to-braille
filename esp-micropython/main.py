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

