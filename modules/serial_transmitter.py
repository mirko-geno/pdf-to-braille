from serial import Serial
try:
    from modules.translator import Braille_translator
except ModuleNotFoundError:
    from translator import Braille_translator


class Transmitter(Braille_translator):
    def __init__(self, port, baudrate):
        super().__init__()
        self.serial = Serial(port, baudrate) # Must use baudrate of 115200 if using ESP8266

    def send(self, letter):
        data = self.translate(letter)
        data = data.to_bytes(1, 'big')  # bits to byte object
        self.serial.write(data)
        print(f'Translation sent: {data}')

    def close(self):
        self.serial.close()


if __name__ == '__main__':
    t = Transmitter(port='/dev/ttyACM0', baudrate=115200)
    t.send("a")