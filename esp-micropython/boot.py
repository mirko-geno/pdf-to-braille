from machine import Pin
from micropython import kbd_intr, const
kbd_intr(-1)

internal_led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)

