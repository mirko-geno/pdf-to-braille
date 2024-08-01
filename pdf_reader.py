import pymupdf
from time import time, sleep

class Reader:
    def __init__(self, path, reading_freq):
        self.pdf = pymupdf.open(path)
        self.reading_freq = reading_freq
        self.titles = self.pdf.get_toc()
        self.page_count = self.pdf.page_count

        self.__page_idx = 0
        self.__block_idx = 0
        self.__letter_idx = 0

    '''def page_data(self, page_num):
        links = self.pdf[page_num].get_links()
        page_text = self.pdf[page_num].get_text('text')
        blocks = self.pdf[page_num].get_text('blocks')
        words = self.pdf[page_num].get_text('words')
        annotations = self.pdf[page_num].annots()
        widgets = self.pdf[page_num].widgets()
        image = self.pdf[page_num].get_pixmap()

        return links, page_text, blocks, words, annotations, widgets, image'''

    def __advance(self):
        BLOCK_TEXT = 4
        while self.__page_idx < self.pdf.page_count:
            reg_time = time()
            self.__block_idx = 0
            blocks = [block[BLOCK_TEXT] for block in self.pdf[self.__page_idx].get_text('blocks')]
            while self.__block_idx < len(blocks):
                self.__letter_idx = 0
                while self.__letter_idx < len(blocks[self.__block_idx]):
                    if time() > (reg_time + 1/self.reading_freq):
                        print(blocks[self.__block_idx][self.__letter_idx])
                        reg_time = time()
                        print(f'letter: {self.__letter_idx}')
                        self.__letter_idx += 1
                print(f'block: {self.__block_idx}')
                self.__block_idx += 1
            print(f'page: {self.__page_idx}')
            self.__page_idx += 1


    def read(self):
        try: self.__advance()
        except KeyboardInterrupt:
            print('Key interrupt')
            sleep(10)
            self.__advance()
