# main
from time import sleep
import select
import sys

while flash_button.value():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:  # Only reads if theres something in the port
        byte = sys.stdin.buffer.read(1)  # Reads a byte from the serial port
        data_int = int.from_bytes(byte, 'big')
        internal_led.value(0)
        internal_led.value(1)

        for i in range(OUT_LEDS):
            led_state = (data_int >> i) & 1  # Shift the i-th bit to the right and extract the least significant bit
            print(f'{i}. led_state: {led_state}')
            led_pins[i].value(led_state)

    sleep(0.1)

for led in led_pins:
    led.value(0)