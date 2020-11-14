import mmap
from collections import Counter
from nltk.corpus import stopwords
import math


class Parsing:

    def getBDoc(self):
        return ["<" + self.doc + ">", "</" + self.doc + ">"]

    def getBDocNo(self):
        return ["<" + self.docno + ">", "</" + self.docno + ">"]

    def __init__(self, doc="doc", docn="docno"):
        self.doc = doc
        self.docno = docn
        self.docParse = dict()
        self.idf = dict()

    def parse(self, document, lang="english"):
        f = mmap.mmap(document.fileno(), 0, access=mmap.ACCESS_READ)
        doc = 0  # doc position
        stop_words = set(stopwords.words(lang))
        while doc != -1:
            doc = f.find(bytes(self.getBDoc()[0], "utf-8"))
            doce = f.find(bytes(self.getBDoc()[1], "utf-8"))
            docn = f.find(bytes(self.getBDocNo()[0], "utf-8"))
            docne = f.find(bytes(self.getBDocNo()[1], "utf-8"))
            words = f[doc:doce].decode("utf-8").replace("\n", " ").split(" ")
            filteredDoc = [w.replace(" ", "") for w in words if not w in stop_words if w.isalpha()]
            if docn != -1 and docne != -1:
                filtered = dict((i, j) for (i, j) in Counter(filteredDoc).items())
                self.docParse[f[docn + 7:docne].decode("utf-8").replace(" ", "")] = filtered
                for t in filtered.keys():  # idf
                    if t in self.idf:
                        self.idf[t] += 1
                    else:
                        self.idf[t] = 1
            f.seek(doce + 1)

        return self.docParse

    def getTf(self, docNo, term):
        return 1 + math.log(self.docParse.get(docNo).get(term), 10)

    def getIdf(self, term):
        return math.log(len(self.docParse) / self.idf[term], 10)

    def getWeight(self, docNo, term):
        return self.getTf(docNo, term) * self.getIdf(term)
