import glob
import logging
import os
import sys
import time
from threading import Thread

import nltk
import xmltodict
from keras_preprocessing.text import text_to_word_sequence

from src.parser import clean_text, getFullText, search
from nltk.corpus import stopwords
from colorama import Fore
nltk.download('stopwords', quiet=True)


class XmlsParser():
    def __init__(self, xmls):
        self.xmls = xmls
        self.corpus = dict()
        self.corpusWcount = dict()

    def parse(self, lang="english", verbose=True):
        sec = 0.1
        xmls = glob.glob(self.xmls + "/*.xml")
        stop_words = set(stopwords.words(lang))
        threads = []
        timer = time.time()
        for xml in xmls:
            thread = XmlParser(xml, stop_words, self.corpus, self.corpusWcount)
            thread.start()
            threads.append(thread)
            t2 = time.time()
            if verbose : #and (t2 - timer > sec or len(threads) == len(xmls)):
                #timer = t2
                percent = (len(threads) / len(xmls)) * 100
                print("\r{}files reading : {} {} {} {:3.2f}%".format(Fore.CYAN,Fore.BLUE, xml, Fore.RED if percent <100 else Fore.LIGHTGREEN_EX, percent), end='')

        print(Fore.RESET)
        while len(threads) > 0:
            for thread in threads:
                if not thread.is_alive():
                    thread.join()
                    threads.remove(thread)
        return self.corpus


class XmlParser(Thread):
    def __init__(self, xml, stop_words, corpus, corpusWcount):
        Thread.__init__(self)
        self.xml = xml
        self.stop_words = stop_words
        self.corpus = corpus
        self.corpusWcount = corpusWcount

    def run(self):
        with open(self.xml, encoding="utf-8") as fd:
            tree = xmltodict.parse(fd.read(), xml_attribs=False, force_list=True)
            document = getFullText(tree)
            doc_id = search(tree, "id")[0]
            text = clean_text(document)
            words = text_to_word_sequence(text)
            filtered_doc = [w.lower() for w in words if not w in self.stop_words and w != '' and w.isalpha()]
            self.corpus[doc_id] = dict((i, j) for (i, j) in nltk.Counter(filtered_doc).items())
            self.corpusWcount[doc_id] = filtered_doc
