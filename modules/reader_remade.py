import pymupdf
from time import time, sleep
from threading import Thread
import keyboard
import re
from modules.serial_transmitter import Transmitter

BLOCK_TEXT = 4
KEY_DELAY = 0.05
OPERATION_DELAY = 0.3

class Reader(Transmitter):
    def __init__(self, path, reading_freq, port, baudrate):
        super().__init__(port, baudrate)
        self.pdf = pymupdf.open(path)
        self.reading_freq = reading_freq
        self.titles = self.pdf.get_toc()
        self.cont_reading = True
        self.__kill_thread = False

        self.__page_idx = 0
        self.__block_idx = 0
        self.__word_idx = 0
        self.__letter_idx = 0

    def quit(self):
        print('Quitting program')
        self.cont_reading = False
        self.__kill_thread = True
        return

    def pause(self):
        print('Pausing lecture')
        self.cont_reading = False
        sleep(OPERATION_DELAY)
    
    def resume(self):
        print('Resuming lecture')
        self.cont_reading = True
        sleep(OPERATION_DELAY)


    def __get_page_blocks(self):
        self.__blocks = [block[BLOCK_TEXT] for block in self.pdf[self.__page_idx].get_text('blocks')]

    def __get_block(self):
        self.__block = self.__blocks[self.__block_idx].replace('/n', ' ')
        self.__block = re.findall(r'\S+', self.__block)
        self.__block = [word + ' ' for word in self.__block[:-1]] + [self.__block[-1]]

    def __get_word(self):
        self.__word = self.__block[self.__word_idx]


    def __forward_page(self):
        if self.__page_idx < self.pdf.page_count -1:
            self.__page_idx += 1
            self.__block_idx = 0
            self.__word_idx = 0
            self.__letter_idx = 0
        else:
            print('Unable to forward more')

    def __forward_block(self):
        if self.__block_idx < len(self.__blocks) -1:
            self.__block_idx += 1
            self.__word_idx = 0
            self.__letter_idx = 0
        else:
            self.__forward_page()
    
    def __forward_word(self):
        if self.__word_idx < len(self.__block) -1:
            self.__word_idx += 1
            self.__letter_idx = 0
        else:
            self.__forward_block()



    def __forward_letter(self):
        if self.__letter_idx < len(self.__word) -1:
            self.__letter_idx += 1
        else:
            self.__forward_word()



    def forward(self):
        self.pause()
        print('Select how to forward:\np for page | b for block | w for wordd | l for letter')
        print(f'page_idx: {self.__page_idx}\nblock_idx: {self.__block_idx}\nword_idx: {self.__word_idx}\nletter_idx: {self.__letter_idx}')
        match keyboard.read_key():
            case 'p':
                print('forward page')
                self.__forward_page()
            case 'b':
                print('forward block')
                self.__forward_block()
            case 'w':
                print('forward word')
                self.__forward_word()
            case 'l':
                print('forward letter')
                self.__forward_letter()
        sleep(KEY_DELAY)


    def __back_page(self, letter_carry=False, word_carry=False, block_carry=False):
        print(f'page_idx: {self.__page_idx}')
        if self.__page_idx:
            self.__page_idx -= 1
            print(f'page_idx after sub: {self.__page_idx}')

            if not (block_carry or word_carry or letter_carry):
                self.__block_idx = 0
                self.__word_idx = 0
                self.__letter_idx = 0

            elif block_carry and not (word_carry or letter_carry):
                self.__word_idx = 0
                self.__letter_idx = 0
                self.__get_page_blocks()
                self.__block_idx = len(self.__blocks) -1

            elif block_carry and word_carry and not letter_carry:
                self.__letter_idx = 0
                self.__get_page_blocks()
                self.__block_idx = len(self.__blocks) -1
                self.__get_block()
                self.__word_idx = len(self.__block) -1

            elif block_carry and word_carry and letter_carry:
                self.__get_page_blocks()
                self.__block_idx = len(self.__blocks) -1
                self.__get_block()
                self.__word_idx = len(self.__block) -1
                self.__get_word()
                self.__letter_idx = len(self.__word) - 1

        else:
            print('Already at the beginning, starting over...\n\n')
            self.__block_idx = 0
            self.__word_idx = 0
            self.__letter_idx = 0

    def __back_block(self, letter_carry=False, word_carry=False):
        print(f'block_idx:{self.__block_idx}')
        if self.__block_idx:
            self.__block_idx -= 1

            if not (word_carry or letter_carry):
                self.__word_idx = 0
                self.__letter_idx = 0

            elif word_carry and not letter_carry:
                self.__letter_idx = 0
                self.__get_block()
                self.__word_idx = len(self.__block) -1

            elif word_carry and letter_carry:
                self.__get_block()
                self.__word_idx = len(self.__block) - 1
                self.__get_word()
                self.__letter_idx = len(self.__word) - 1

        else:
            if not (letter_carry or word_carry):
                self.__back_page(block_carry=True)

            elif word_carry and not letter_carry:
                self.__back_page(word_carry=True, block_carry=True)

            elif word_carry and letter_carry:
                self.__back_page(letter_carry=True, word_carry=True, block_carry=True)

    def __back_word(self, letter_carry=False):
        print(f'Word_idx: {self.__word_idx}')
        if self.__word_idx:
            self.__word_idx -= 1

            if not letter_carry:
                self.__letter_idx = 0

            elif letter_carry:
                self.__get_word()
                self.__letter_idx = len(self.__word) -1

        else:
            if not letter_carry:
                self.__back_block(word_carry=True)

            elif letter_carry:
                self.__back_block(letter_carry=True, word_carry=True)
    
    def __back_letter(self):
        if self.__letter_idx:
            self.__letter_idx -= 1
        else: self.__back_word(letter_carry=True)


    def back(self):
        self.pause()
        print('Select how to back:\np for page | b for block | w for word | l for letter')
        print(f'page_idx: {self.__page_idx}\nblock_idx: {self.__block_idx}\nword_idx: {self.__word_idx}\nletter_idx: {self.__letter_idx}')
        match keyboard.read_key():
            case 'p':
                print('back page')
                self.__back_page()
            case 'b':
                print('back block')
                self.__back_block()
            case 'w':
                print('back word')
                self.__back_word()
            case 'l':
                print('back letter')
                self.__back_letter()
        sleep(KEY_DELAY)

    
    def __adv_page(self):
        while self.__page_idx < self.pdf.page_count and self.cont_reading:
            self.__blocks = [block[BLOCK_TEXT] for block in self.pdf[self.__page_idx].get_text('blocks')]
            self.__adv_block()
            if self.cont_reading:
                self.__block_idx = 0
                self.__page_idx += 1


    def __adv_block(self):
        while self.__block_idx < len(self.__blocks) and self.cont_reading:
            self.__block = self.__blocks[self.__block_idx].replace('/n', ' ')
            self.__block = re.findall(r'\S+', self.__block)
            if len(self.__block):
                self.__block = [word + ' ' for word in self.__block[:-1]] + [self.__block[-1]]   
            self.__adv_word()
            if self.cont_reading:
                self.__word_idx = 0            
                self.__block_idx += 1


    def __adv_word(self):
        while self.__word_idx < len(self.__block) and self.cont_reading:
            self.__word = self.__block[self.__word_idx]
            count = 0
            if not count:
                print(f'word: {self.__word}   word_idx: {self.__word_idx}')
                count += 1
            self.__adv_letter()
            if self.cont_reading:
                self.__letter_idx = 0
                self.__word_idx += 1
        
            
    def __adv_letter(self):
        while self.__letter_idx < len(self.__word) and self.cont_reading:
            if time() > (self.__reg_time + 1/self.reading_freq):
                letter = self.__word[self.__letter_idx]
                self.send(letter)
                print(letter)
                self.__reg_time = time()
                if self.cont_reading:
                    self.__letter_idx += 1


    def __advance(self):
        while not self.__kill_thread:
            sleep(0.1)
            self.__reg_time = time()
            self.__adv_page()

            if self.__kill_thread:
                print("Finished reading\nClosing program...")
                self.quit()


    def read(self):
        self.__read_thread = Thread(target=self.__advance)
        self.__read_thread.start()

        while self.__read_thread.is_alive():
            match keyboard.read_key():
                case 'q':
                    self.quit()
                case 'p':
                    self.pause()
                case 'r':
                    self.resume()
                case 'b':
                    self.back()
                case 'f':
                    self.forward()
            sleep(KEY_DELAY)
