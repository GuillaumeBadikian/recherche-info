import json
import math
import mmap
import os
import re
from collections import Counter

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class Rank:
    def __init__(self, vectorModel):
        self.vectorModel = vectorModel
        self.scoreList = []

    def getDocsNo(self):
        return list(dict.fromkeys([i[0] for i in self.vectorModel.keys()]))

    #def scoreAndGenerate(self,queryName, staffName, step, *query):
    def scoreAndGenerate(self, staff,step,run, weighting,granularity, params, *query):
        for i in query:
           for(j,k) in i.items():
               self.score(k)
               self.generateRuns(staff,step,run,j,weighting,granularity,params)


    def score(self, query):
        self.scoreList = []
        for doc in self.getDocsNo():
            currentDoc = [doc, 0]
            for term in query:
                if (doc, term) in self.vectorModel:
                    currentDoc[1] += self.vectorModel[doc, term]
            self.insertDocScoreSorted(currentDoc)
        return self.scoreList

    def insertDocScoreSorted(self,newScore):
        for i in range(0, len(self.scoreList)):
            if self.scoreList[i][1] < newScore[1]:
                self.scoreList.insert(i, newScore)
                return
        self.scoreList.append(newScore)

    def generateRuns(self,staff,step,run,queryId, weighting='ltn',granularity = "articles", params=None):
        #f = open("runs/run_" + staffName + ".txt", "w")
        f = open("runs/{}_{}_{}_{}_{}_{}.txt".format(staff,step,run,weighting,granularity,params ), "a")
        rank = 1

        path = "/article[1]"
        coef = 1 / self.scoreList[0][1]
        runs = ""
        for docScore in self.scoreList:
            # currentRun = queryName + "Q0" + docScore[0] * coef + docScore[1] + staffName + path
            currentRun = f'{queryId} {step} {docScore[0]} {rank} {str(docScore[1])} {staff} {path}'
            runs += currentRun + "\n"
            rank += 1
            if rank>1500: break
        f.write(runs)
        f.close()


class VectorModel:

    def __init__(self, corpus):
        self.corpus = corpus
        self.vectorModel = dict()

    def createVector(self):
        w = 0
        for (i, j) in self.corpus.items():
            for (k, l) in j.items():
                self.vectorModel[(i, k)] = self.getWeight(i, k)
            w += 1

        return self.vectorModel

    def toJson(self, dest: str):
        if self.vectorModel:
            l = []
            for (i, j) in self.vectorModel.items():
                l.append([i[0], i[1], j])
            data = json.dumps(l)
            with open(dest, 'w') as f:
                f.write(data)

    def getVectorModelList(self):
        if self.vectorModel:
            l = []
            for (i, j) in self.vectorModel.items():
                l.append([i[0], i[1], j])
            return l
        return None
    def fromJson(self, fr: str):
        with open(fr, 'r') as f:
            vector = json.load(f)
            for i in vector:
                self.vectorModel[(i[0], i[1])] = i[2]

    def getTf(self, docNo, term):
        return (math.log2(self.corpus.get(docNo).get(term))+1) / (math.log2(len(self.corpus.get(docNo))))
        #return 1 + math.log(self.corpus.get(docNo).get(term), 10)

    def getIdf(self, term):
        return math.log2(1+ len(self.corpus) / self.idf[term])

    def getWeight(self, docNo, term):
        return self.getTf(docNo, term) * self.getIdf(term)


class Parser(VectorModel, Rank):

    def __init__(self, doc=["<doc>", "</doc>"], docNo=["<docno>", "</docno>"]):
        self.doc = doc
        self.docNo = docNo
        self.corpus = dict()
        self.idf = dict()
        self.vectorModel = dict()

    def parse(self, corpus, lang="english", parser="[\w'/():\"@+-]*"):
        file = mmap.mmap(corpus.fileno(), 0, access=mmap.ACCESS_READ)
        doc = 0

        while (doc != -1):  # end file
            doc = file.find(bytes(self.doc[0], "utf-8"))
            doce = file.find(bytes(self.doc[1], "utf-8"))
            docn = file.find(bytes(self.docNo[0], "utf-8"))
            docne = file.find(bytes(self.docNo[1], "utf-8"))

            if docn != -1 and docne != -1:
                docs = file[docne + len(self.docNo[1]):doce].decode("utf-8")
                filtered = self.parseDoc(docs, lang, parser)
                self.corpus[file[docn + 7:docne].decode("utf-8")] = filtered
                for i in filtered.keys():
                    if i in self.idf:
                        self.idf[i] += 1
                    else:
                        self.idf[i] = 1

            file.seek(doce + 1)
        return self.corpus

    def parseDoc(self, document, lang="english", parser="[\w'/():\"]*"):
        stop_words = set(stopwords.words(lang))
        parse = re.compile(parser)
        words = parse.findall(document)
        #lemmatizer = WordNetLemmatizer()
        #from nltk.stem import PorterStemmer
        #ps = PorterStemmer()
        #[ps.stem(w) for w in words]
        #[lemmatizer.lemmatize(w) for w in words]
        #words = document.replace("\n", " ").split(" ")
        filteredDoc = [w.lower() for w in words if not w in stop_words and w != '' and w.isalpha()]
        return dict((i, j) for (i, j) in Counter(filteredDoc).items())
