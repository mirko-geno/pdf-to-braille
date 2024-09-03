# boot
from machine import Pin
from micropython import kbd_intr, const
kbd_intr(-1)

OUT_LEDS = const(8)
BITS = const([14, 15, 4, 13, 5, 16, 12, 10])

'''
[BIT 7 = PIN 10] [BIT 5 = PIN 16]
[BIT 6 = PIN 12] [BIT 4 = PIN 5 ]
[BIT 3 = PIN 13] [BIT 2 = PIN 4 ]
[BIT 1 = PIN 15] [BIT 0 = PIN 14]

'''

internal_led = Pin(2, Pin.OUT)
flash_button = Pin(0, Pin.IN, Pin.PULL_UP)


led_pins = [Pin(BITS[7], Pin.OUT),
            Pin(BITS[6], Pin.OUT),
            Pin(BITS[5], Pin.OUT),
            Pin(BITS[4], Pin.OUT),
            Pin(BITS[3], Pin.OUT),
            Pin(BITS[2], Pin.OUT),
            Pin(BITS[1], Pin.OUT),
            Pin(BITS[0], Pin.OUT)]


# main
from time import sleep
import select
import sys

while flash_button.value():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:  # Only reads if theres something in the port
        byte = sys.stdin.buffer.read(1)  # Reads a byte from the serial port
        data_int = int.from_bytes(byte, 'big')
        # print(f'Byte received: {byte}')
        internal_led.value(not internal_led.value())

        for i in range(OUT_LEDS):
            led_state = (data_int >> i) & 1  # Desplaza el bit i hacia la derecha y extrae el bit menos significativo
            print(f'{i}. led_state: {led_state}')
            # led_pins[i].value(led_state)  # Establece el estado del LED basado en el bit correspondiente

    sleep(0.1)
