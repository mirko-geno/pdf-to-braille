from machine import Pin, UART #type: ignore
from time import sleep

led=Pin(2,Pin.OUT)
uart = UART(0, 460800)
uart.init()

value = 0
while True:
    if uart.any():
        led.value(value)
        value = not value
    sleep(0.1)
