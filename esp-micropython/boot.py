# boot
from machine import Pin
from micropython import kbd_intr, const
kbd_intr(-1)

OUT_LEDS = const(8)
BITS = [14, 15, 4, 13, 5, 16, 12, 1]
'''
[BIT 7 = PIN 14] [BIT 5 = PIN 4 ]
[BIT 6 = PIN 15] [BIT 4 = PIN 13]
[BIT 3 = PIN 5 ] [BIT 2 = PIN 16]
[BIT 1 = PIN 12] [BIT 0 = PIN 1 ]

'''
internal_led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)

led_pins = [Pin(BITS[0], Pin.OUT),
            Pin(BITS[1], Pin.OUT),
            Pin(BITS[2], Pin.OUT),
            Pin(BITS[3], Pin.OUT),
            Pin(BITS[4], Pin.OUT),
            Pin(BITS[5], Pin.OUT),
            Pin(BITS[6], Pin.OUT),
            Pin(BITS[7], Pin.OUT)]

for led in led_pins:
    led.value(0)