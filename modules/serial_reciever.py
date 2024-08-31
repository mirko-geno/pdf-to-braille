from machine import Pin
from time import sleep
import micropython
import select
import sys

led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)

micropython.kbd_intr(-1)

while flash_button.value():
    ch = sys.stdin.read(1)

    if ch == 'Q':
        led.value(not led.value())
    else:
        pass

    sleep(0.1)