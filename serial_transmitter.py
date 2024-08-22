import serial

class Transmitter():
    def __init__(self, port):
        self.port = serial.Serial(port)
    
    def send(self, letter):
        self.port.write(letter)