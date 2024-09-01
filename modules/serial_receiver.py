# boot
from machine import Pin
from micropython import kbd_intr, const
kbd_intr(-1)

OUT_LEDS = const(8)

internal_led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)

led_pins = [Pin(10, Pin.OUT),
            Pin(9, Pin.OUT),
            Pin(16, Pin.OUT),
            Pin(5, Pin.OUT),

            Pin(4, Pin.OUT),
            Pin(2, Pin.OUT),
            Pin(14, Pin.OUT),
            Pin(12, Pin.OUT),]


# main
from time import sleep
import select
import sys

while flash_button.value():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:  # Only reads if theres something in the port
        byte = sys.stdin.buffer.read(1)  # Reads a byte from the serial port
        # print(f'Byte received: {byte}')
        if byte == b'\x98':
            internal_led.value(not internal_led.value())

        for i in range(OUT_LEDS):
            led_state = (byte >> i) & 1  # Desplaza el bit i hacia la derecha y extrae el bit menos significativo
            led_pins[i].value(led_state)  # Establece el estado del LED basado en el bit correspondiente

    sleep(0.1)
