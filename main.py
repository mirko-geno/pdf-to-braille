from modules.reader_remade import Reader

def main():
    print('Inciando programa...\nLeyendo archivo PDF')    
    pdf_reader = Reader(path='sample_pdfs/Yo, robot - Isaac Asimov.pdf', reading_freq=3, port='/dev/ttyACM0', baudrate=230400)

    print('PDF leído exitosamente\n Iniciando lectura...\n\n\n')
    pdf_reader.read()


main()
