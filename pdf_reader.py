import pymupdf
from time import time, sleep

class Reader:
    def __init__(self, path, reading_freq):
        self.pdf = pymupdf.open(path)
        self.reading_freq = reading_freq
        self.titles = self.pdf.get_toc()
        self.page_count = self.pdf.page_count

    '''def page_data(self, page_num):
        links = self.pdf[page_num].get_links()
        page_text = self.pdf[page_num].get_text('text')
        blocks = self.pdf[page_num].get_text('blocks')
        words = self.pdf[page_num].get_text('words')
        annotations = self.pdf[page_num].annots()
        widgets = self.pdf[page_num].widgets()
        image = self.pdf[page_num].get_pixmap()

        return links, page_text, blocks, words, annotations, widgets, image'''

    def advance(self):
        for block_i, block in enumerate(blocks):
            for word_i, word in enumerate(block[4]):
                for letter in word:
                    reg_time = time() # yo  no
                    print(letter)
                    while reg_time + 1/reading_freq > time():pass

    def read(self):
        self.__page_i = 0
        self.__block_i = 0
        self.__word_i = 0
        reg_time = time()

        while True:
            if time() >= reg_time + 1/reading_freq:
                print()
