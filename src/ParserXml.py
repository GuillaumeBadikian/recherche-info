import glob
import re
from collections import Counter
from xml.etree import ElementTree
from xml.dom import minidom
from threading import Thread

import xmltodict
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
        with open(self.xml, encoding="utf-8") as fd:
            tree = xmltodict.parse(fd.read(), xml_attribs=False, force_list=True)
            #tree = ElementTree.parse(source=self.xml, parser=self.getParser())
            # print(tree.getroot())
            document = self.parc(tree)

            #document = " ".join(list(filter(None.__ne__, document)))
            #doc_id = [i.text for i in tree.iter('id')][0]
            doc_id = self.search(tree,"id")[0]
            parser = re.compile(self.parser)
            words = parser.findall(document)
            ps = PorterStemmer()
            #[ps.stem(w) for w in words]
            lemmatizer = WordNetLemmatizer()

            #[lemmatizer.lemmatize(w) for w in words]
            filteredDoc = [lemmatizer.lemmatize(ps.stem(w.lower())) for w in words if not w in self.stop_words and w != '' ]
            self.corpus[doc_id] = dict((i, j) for (i, j) in Counter(filteredDoc).items())
            for i in self.corpus[doc_id].keys():
                if i in self.idf:
                    self.idf[i] += 1
                else:
                    self.idf[i] = 1

    def parc(self, doc):
        l1 = []
        self.parc2(doc, l1)
        return " ".join(l1)

    def parc2(self, doc, l):
        if isinstance(doc, dict):
            for (k, v) in doc.items():
                self.parc2(v, l)
        elif isinstance(doc, list):
            for i in doc:
                self.parc2(i, l)

        elif isinstance(doc, str):
            l.append(doc)
        return l

    def search2(self, st, w, p, q):
        """
        search recursively a string into a Dict : Key or Value
        :param st: String to search
        :param w: Dict where search
        :param p: List of string of n-1 path into Dict (overTree)
        :param q: List of string which contains path where st has been found
        :return: List of path where st found
        """
        if isinstance(w, list):
            for a, i in enumerate(w,0):
                if(isinstance(i,dict) or isinstance(i,list)):
                    p.append(a)
                self.search2(st, i, p, q)

        elif isinstance(w, dict):
            for (k, v) in w.items():
                if k == st or v == st:
                    #q.append(copy.deepcopy(p))
                    q.append(v[0])
                p.append(k)
                self.search2(st, v, p, q)
                p.remove(k)  # rm sub trees when up


        return q

    def search(self, doc, st):
        """
        :param st: string to search
        :return: List of path where st found
        """
        t = []
        q = []
        w = doc
        self.search2(st, w, t, q)
        return q

    def docToText(self,doc):
        if isinstance(doc,dict):
            for (k,v )in doc.items():
                self.te(v)
        elif isinstance(doc,list):
            for i in doc:
                self.te(i)
        elif isinstance(doc, str):
            print(doc)

class ParserXmls(VectorModel, Rank):

    def __init__(self, xmls):
        self.xmls = xmls
        self.corpus = dict()
        self.idf = dict()
        self.vectorModel = dict()
        self.indent = 0
        self.v = []

    def printRecur(self, root):
        """Recursively prints the tree."""
        self.v.append(root.text)
        print(' ' * self.indent + '%s: %s' % (root.tag.title(), root.attrib.get('name', root.text)))
        self.indent += 4
        for elem in root.getchildren():
            self.printRecur(elem)
        self.indent -= 4

    def parse(self, lang="english", parser="[\w'/():\"@+-]*", verbose=True):
        xmls = glob.glob(self.xmls + "/*.xml")
        stop_words = set(stopwords.words(lang))
        threads = []
        for xml in xmls:
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
