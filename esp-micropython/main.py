from time import sleep
import sys
import select

while flash_button.value():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:  # Only reads if theres something in the port
        byte = sys.stdin.buffer.read(1)  # Reads a byte from the serial port
        # print(f'Byte received: {byte}')
        if byte == b'\x98':
            internal_led.value(not internal_led.value())
    sleep(0.1)
