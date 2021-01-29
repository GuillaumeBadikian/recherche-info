from nltk.corpus import stopwords


class XmlRank:
    def __init__(self, corpus):
        self.corpus = corpus
        self.bm25 = []

    def getBm25(self, request,func, k=1.5, b=0.75, d=0.5):
        request = [i for i in request if  i not in set(stopwords.words("english"))]

        doc_scores = func(self.corpus.values(),request, k,b,d)
        ret = list(zip(self.corpus.keys(), doc_scores))
        self.bm25 = sorted(ret, key=lambda x: x[1], reverse=True)
        return self.bm25

    def getBm25_2(self, request,func, k=1.5, b=0.75, d=0.5):
        print(self.corpus)
