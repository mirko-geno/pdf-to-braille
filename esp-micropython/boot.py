# boot
from machine import Pin
from micropython import kbd_intr, const
kbd_intr(-1)

OUT_LEDS = const(8)

internal_led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)

led_pins = [Pin(10, Pin.OUT),
            Pin(16, Pin.OUT),
            Pin(5, Pin.OUT),
            Pin(4, Pin.OUT),

            Pin(14, Pin.OUT),
            Pin(12, Pin.OUT),
            Pin(13, Pin.OUT),
            Pin(15, Pin.OUT)]