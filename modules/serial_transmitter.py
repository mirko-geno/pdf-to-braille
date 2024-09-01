from serial import Serial
from modules.translator import Braille_translator


class Transmitter():
    def __init__(self, port, baudrate):
        self.serial = Serial(port, baudrate) # Must use baudrate of 115200 if using ESP8266
        self.translator = Braille_translator()

    def send(self, letter):
        data = self.translator.translate(letter)
        data = data.to_bytes(1, 'big')  # bits to byte object
        self.serial.write(data)
        print(f'Translation sent: {data}')

    def close(self):
        self.serial.close()
