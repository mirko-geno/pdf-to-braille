from pdf_reader import Reader


def main():
    print('Inciando programa...\nLeyendo archivo PDF')    
    pdf_reader = Reader(path='Yo, robot - Isaac Asimov.pdf', reading_freq=2)
    print('PDF leído exitosamente\n Iniciando lectura...\n\n\n')
    pdf_reader.read()


main()