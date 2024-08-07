import pymupdf
from time import time, sleep
from threading import Thread
import keyboard
import re


class Reader:
    def __init__(self, path, reading_freq):
        self.pdf = pymupdf.open(path)
        self.reading_freq = reading_freq
        self.titles = self.pdf.get_toc()
        self.cont_reading = True
        self.__kill_thread = False

        self.__page_idx = 0
        self.__block_idx = 0
        self.__word_idx = 0
        self.__letter_idx = 0


    def __quit(self):
        print('Quitting program')
        self.cont_reading = False
        self.__kill_thread = True
        self.__read_thread.join()

    def __pause(self):
        print('Pausing lecture')
        self.cont_reading = False
        sleep(0.05)
    
    def __resume(self):
        print('Resuming lecture')
        self.cont_reading = True
        sleep(0.05)



    def __last_block(self):
        if self.__word_idx > 0:
            self.__word_idx -= 1
            self.__letter_idx = len(word)-1
            # self.__resume()
        else:
            self.__back_block()

    def __back_page(self):
        self.__pause()
        self.__block_idx = 0
        self.__word_idx = 0
        self.__letter_idx = 0
        if self.__page_idx > 0:
            print('Going one page back')
            self.__page_idx -= 1
        else: print('Already in first page')
        # self.__resume()

    def __back_block(self):
        self.__pause()
        if self.__block_idx > 0:
            print('Going one page back')
            self.__word_idx = 0
            self.__letter_idx = 0
            self.__block_idx -= 1
            # self.__resume()
        else:
            self.__back_page()

    def __back_word(self):
        self.__pause()
        if self.__word_idx > 0:
            print('Going back one word')
            self.__letter_idx = 0
            self.__word_idx -= 1
            # self.__resume()
        else:
            self.__back_block()

    def __back_letter(self):
        self.__pause()
        if self.__letter_idx > 0:
            print('Going back one letter')
            self.__letter_idx -= 1
            # self.__resume()
        else:
            self.__back_word()


    def __advance(self):
        BLOCK_TEXT = 4
        while not self.__kill_thread:
            sleep(0.1)
            reg_time = time()
            while self.__page_idx < self.pdf.page_count and self.cont_reading:
                self.__block_idx = 0
                blocks = [block[BLOCK_TEXT] for block in self.pdf[self.__page_idx].get_text('blocks')]

                while self.__block_idx < len(blocks) and self.cont_reading:
                    self.__word_idx = 0
                    block = blocks[self.__block_idx].replace('/n', ' ')
                    block = re.findall(r'\S+', block)
                    block = [word + ' ' for word in block[:-1]] + [block[-1]]

                    while self.__word_idx < len(block) and self.cont_reading:
                        self.__letter_idx = 0
                        word = block[self.__word_idx]
                        count = 0
                        if not count:
                            print(word)
                            count +=1

                        while self.__letter_idx < len(word) and self.cont_reading:
                            if time() > (reg_time + 1/self.reading_freq):
                                print(word[self.__letter_idx])
                                reg_time = time()
                                self.__letter_idx += 1
                        self.__word_idx += 1                    
                    self.__block_idx += 1
                self.__page_idx += 1


    def read(self):
        self.__read_thread = Thread(target=self.__advance)
        self.__read_thread.start()

        while self.__read_thread.is_alive():
            match keyboard.read_key():
                case 'q':
                    self.__quit()
                case 'p':
                    self.__pause()
                case 'r':
                    self.__resume()
                case 'f':
                    self.__back_page()
                case 'g':
                    self.__back_block()
                case 'h':
                    self.__back_word()
                case 'j':
                    self.__back_letter()
            sleep(0.05)
