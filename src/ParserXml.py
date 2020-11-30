import glob
import re
from collections import Counter
from xml.etree import ElementTree
from threading import Thread

from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk

from src import Parser
from src.Parser import VectorModel, Rank


class ParseXml(Thread):

    def __init__(self, xml, stop_words, parser, corpus, idf):
        Thread.__init__(self)
        self.xml = xml
        self.stop_words = stop_words
        self.parser = parser
        self.corpus = corpus
        self.idf = idf

    def getParser(self):
        parser = ElementTree.XMLParser()
        parser.entity['nbsp'] = " "
        parser.entity['mdash'] = " "
        parser.entity['ndash'] = " "
        parser.entity['middot'] = " "
        parser.entity['lsaquo'] = " "
        parser.entity['rsaquo'] = " "
        return parser

    def run(self):
        tree = ElementTree.parse(source=self.xml, parser=self.getParser())
        # print(tree.getroot())
        document = [elem.text for elem in tree.iter()]
        document = " ".join(list(filter(None.__ne__, document)))
        doc_id = [i.text for i in tree.iter('id')][0]
        parser = re.compile(self.parser)
        words = parser.findall(document)
        #ps = PorterStemmer()
        #[ps.stem(w) for w in words]
        lemmatizer = WordNetLemmatizer()
        [lemmatizer.lemmatize(w) for w in words]
        filteredDoc = [w.lower() for w in words if not w in self.stop_words and w != '' and w.isalpha()]
        self.corpus[doc_id] = dict((i, j) for (i, j) in Counter(filteredDoc).items())
        for i in self.corpus[doc_id].keys():
            if i in self.idf:
                self.idf[i] += 1
            else:
                self.idf[i] = 1



class ParserXmls(VectorModel, Rank):

    def __init__(self, xmls):
        self.xmls = xmls
        self.corpus = dict()
        self.idf = dict()
        self.vectorModel = dict()

    def parse(self, lang="english", parser="[\w'/():\"@+-]*", verbose=True):
        xmls = glob.glob(self.xmls + "/*.xml")
        stop_words = set(stopwords.words(lang))
        threads = []
        i = 0
        for xml in xmls:
            print(i)
            i+=1
            thread = ParseXml(xml, stop_words, parser, self.corpus, self.idf)
            thread.start()
            threads.append(thread)

        while len(threads) > 0:
            for thread in threads:
                if not thread.is_alive():
                    thread.join()
                    threads.remove(thread)
            if verbose:
                print("avancement : {:3.2f}%".format((1 - len(threads) / len(xmls)) * 100), flush=True)
        return self.corpus
