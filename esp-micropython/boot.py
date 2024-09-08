# boot
from machine import Pin
from micropython import kbd_intr, const
kbd_intr(-1)

OUT_LEDS = const(8)
PINS = [14, 15, 4, 13, 5, 16, 12, 1]
'''
[BIT 7 = PIN 14] [BIT 5 = PIN 4 ]
[BIT 6 = PIN 15] [BIT 4 = PIN 13]
[BIT 3 = PIN 5 ] [BIT 2 = PIN 16]
[BIT 1 = PIN 12] [BIT 0 = PIN 1 ]

'''
internal_led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)
led_pins = [Pin(pin, Pin.OUT) for pin in PINS]

for led in led_pins:
    led.value(0)
