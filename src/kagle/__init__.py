import re
from collections import Counter

import xmltodict
from nltk.corpus import stopwords


class XmlsParse():
    def __init__(self,xml):
        self.xml = xml
        self.corpus = dict()
        self.corpusWcount = dict()
        self.stop_words = set(stopwords.words("english"))

    def parse(self):
        with open(self.xml, encoding="utf-8") as fd:
            tree = xmltodict.parse(fd.read(), xml_attribs=False, force_list=True)
            document = self.getFullText(tree)
            doc_id = self.search(tree, "id")[0]

            # parser = re.compile(self.parser)
            # words = parser.findall(document)

            words = re.findall("[\w]*", document)
            words = document.split()
            #ps = PorterStemmer()

            filteredDoc = [w.lower() for w in words if not w in self.stop_words and w != '']
            # print([w.lower() for w in words if not w in self.stop_words and w != ''])
            self.corpus[doc_id] = dict((i, j) for (i, j) in Counter(filteredDoc).items())
            self.corpusWcount[doc_id] = filteredDoc

    def getFullText(self, doc):
        l1 = []
        self.getFullTextRec(doc, l1)
        return " ".join(l1)

    def getFullTextRec(self, doc, l):
        if isinstance(doc, dict):
            for (k, v) in doc.items():
                self.getFullTextRec(v, l)
        elif isinstance(doc, list):
            for i in doc:
                self.getFullTextRec(i, l)

        elif isinstance(doc, str):
            l.append(doc)
        return l

    def search(self, doc, st):
        """
        :param st: string to search
        :return: List of path where st found
        """
        t = []
        q = []
        w = doc
        self.searchRec(st, w, t, q)
        return q

    def searchRec(self, st, w, p, q):
        """
        search recursively a string into a Dict : Key or Value
        :param st: String to search
        :param w: Dict where search
        :param p: List of string of n-1 path into Dict (overTree)
        :param q: List of string which contains path where st has been found
        :return: List of path where st found
        """
        if isinstance(w, list):
            for a, i in enumerate(w, 0):
                if (isinstance(i, dict) or isinstance(i, list)):
                    p.append(a)
                self.searchRec(st, i, p, q)

        elif isinstance(w, dict):
            for (k, v) in w.items():
                if k == st or v == st:
                    # q.append(copy.deepcopy(p))
                    q.append(v[0])
                p.append(k)
                self.searchRec(st, v, p, q)
                p.remove(k)  # rm sub trees when up

        return q