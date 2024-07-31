import pymupdf
from time import time, sleep
from pdf_reader import Reader

pdf = pymupdf.open('Yo, robot - Isaac Asimov.pdf')

titles = pdf.get_toc()
page_count = pdf.page_count

page_num = 13
blocks_text = [block[4] for block in pdf[page_num].get_text('blocks')]



links = pdf[page_num].get_links()
page_text = pdf[page_num].get_text('text')

words = pdf[page_num].get_text('words')

annotations = pdf[page_num].annots()

widgets = pdf[page_num].widgets()
image = pdf[page_num].get_pixmap()


