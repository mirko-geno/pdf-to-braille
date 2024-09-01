from modules.reader_remade import Reader

def main():
    print('Inciando programa...\nLeyendo archivo PDF')    
    pdf_reader = Reader(path='Yo, robot - Isaac Asimov.pdf', reading_freq=10, port='/dev/ttyUSB0', baudrate=115200)

    print('PDF leído exitosamente\n Iniciando lectura...\n\n\n')
    pdf_reader.read()


main()
