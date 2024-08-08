import pymupdf
from time import time, sleep
from threading import Thread
import keyboard
import re

BLOCK_TEXT = 4
KEY_DELAY = 0.05


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

    def __forward(self, key):
        if key == 'c':
            pass

    def __get_word(self):
        self.__word = self.__block[self.__word_idx]

    
    def __get_block(self):
        self.__blocks = [block[BLOCK_TEXT] for block in self.pdf[self.__page_idx].get_text('blocks')]
        self.__block = self.__blocks[self.__block_idx].replace('/n', ' ')
        self.__block = re.findall(r'\S+', self.__block)
        self.__block = [word + ' ' for word in self.__block[:-1]] + [self.__block[-1]]


    def __back_block(self, letter_carry=False, word_carry=False):
        if self.__block_idx and not (word_carry and letter_carry):
            self.__word_idx = 0
            self.__letter_idx = 0
            self.__block_idx -= 1

        elif self.__block_idx and word_carry and not letter_carry:
            self.__block_idx -= 1
            self.__get_block()
            self.__word_idx = len(self.__block) -1

        elif self.__block_idx and word_carry and letter_carry:
            self.__block_idx -= 1
            self.__get_block()
            self.__word_idx = len(self.__block) - 1
            self.__get_word()
            self.__word_idx = len(self.__word) - 1



    def __back_word(self, letter_carry=False):
        if self.__word_idx and not letter_carry:
            self.__letter_idx = 0
            self.__word_idx -= 1
        
        elif self.__word_idx and letter_carry:
            self.__word_idx -= 1
            self.__get_word()
            self.__letter_idx = len(self.__word) -1

        elif not self.__word_idx and not letter_carry:
            self.__back_block(word_carry=True)

        elif not self.__word_idx and letter_carry:
            self.__back_block(letter_carry=True, word_carry=True)
            # self.__letter_idx = len(self.__get_block()) -1 # Get to last letter of 

    
    def __back_letter(self):
        if self.__letter_idx:
            self.__letter_idx -= 1
        else: self.__back_word(letter_carry=True)


    def __back(self):
        self.__pause()
        while self.__read_thread.is_alive():
            match keyboard.read_key():
                case 'p':
                    self.__back_page()
                case 'b':
                    self.__back_block()
                case 'w':
                    self.__back_word()
                case 'l':
                    self.__back_letter()
            sleep(KEY_DELAY)
        self.__resume()

    
    def __adv_page(self):
        while self.__page_idx < self.pdf.page_count and self.cont_reading:
            self.__block_idx = 0
            self.__blocks = [block[BLOCK_TEXT] for block in self.pdf[self.__page_idx].get_text('blocks')]
            self.__adv_block()
            self.__page_idx += 1


    def __adv_block(self):
        while self.__block_idx < len(self.__blocks) and self.cont_reading:
            self.__word_idx = 0
            self.__block = self.__blocks[self.__block_idx].replace('/n', ' ')
            self.__block = re.findall(r'\S+', self.__block)
            self.__block = [word + ' ' for word in self.__block[:-1]] + [self.__block[-1]]   
            self.__adv_word()              
            self.__block_idx += 1


    def __adv_word(self):
        while self.__word_idx < len(self.__block) and self.cont_reading:
            self.__letter_idx = 0
            self.__word = self.__block[self.__word_idx]
            count = 0
            if not count:
                print(self.__word)
                count += 1
            self.__adv_letter()
            self.__word_idx += 1
        
            
    def __adv_letter(self):
        while self.__letter_idx < len(self.__word) and self.cont_reading:
            if time() > (self.__reg_time + 1/self.reading_freq):
                print(self.__word[self.__letter_idx])
                self.__reg_time = time()
                self.__letter_idx += 1


    def __advance(self):
        while not self.__kill_thread:
            sleep(0.1)
            self.__reg_time = time()
            self.__adv_page()


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
                case 'b':
                    self.__back()
            sleep(KEY_DELAY)
