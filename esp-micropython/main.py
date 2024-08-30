import micropython
import machine
import select
import sys

led = machine.Pin(2, machine.Pin.OUT)  # El LED interno está en el pin GPIO 2 en el ESP8266
micropython.kbd_intr(-1)

while True:
  while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:        
    ch = sys.stdin.read(1)
    if ch:
        led.value(not led.value())  # Alterna el estado del LED