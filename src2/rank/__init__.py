from colorama import Fore
from nltk import PorterStemmer
from rank_bm25 import BM25Okapi
import os
from datetime import date
import rank_bm25
import math

from src2.parser import keras_tokenize


class Run():
    def __init__(self, staff, step, run, weightingF, granularity, others=[]):
        self.staff = staff
        self.step = step
        self.run = run
        self.weightingFunc = weightingF
        self.granularity = granularity
        self.others = others

    def createRun(self, dir, ranking, queryId, limit=1500, verbose = True):
        d = "{}/{}".format(dir, date.today().strftime("%Y-%m-%d"))
        if not os.path.exists(d):
            os.makedirs(d)
        if verbose:
            print("{}Drafting of the classification of the request id {} {} {} in {} {} {}".format(Fore.CYAN,Fore.GREEN,queryId, Fore.CYAN,Fore.GREEN,d, Fore.RESET))
        f = open("{}/{}".format(d, self.getFormat()), 'a')
        rank = 1
        runs = ""
        path = "/article[1]"
        for r in ranking:
            if rank > limit: break
            current_run = f'{queryId} {self.step} {r[0]} {rank} {str(r[1])} {self.staff} {path}'
            runs += current_run + "\n"
            rank += 1

        f.write(runs)
        f.close()

    def getFormat(self):
        return "{}_{}_{}_{}_{}_{}.txt".format(self.staff, self.step, self.run, self.weightingFunc, self.granularity,
                                              '_'.join(self.others))


class XmlRank():
    def __init__(self, corpus):
        self.corpus = corpus
        self.bm25 = []

    def getBm25(self, request, k=1.5, b=0.75, d=0.5):
        #bm25 = rank_bm25.BM25L(self.corpus.values(), k1=k, b=b, delta=d)
        bm25 = BM25(k1=k, b=b)
        bm25.fit(self.corpus.values())
        doc_scores = bm25.search(request)
        #doc_scores = bm25.get_scores(request)
        ret = list(zip(self.corpus.keys(), doc_scores))
        self.bm25 = sorted(ret, key=lambda x: x[1], reverse=True)
        return self.bm25


class BM25:
    """
    Best Match 25.

    Parameters
    ----------
    k1 : float, default 1.5

    b : float, default 0.75

    Attributes
    ----------
    tf_ : list[dict[str, int]]
        Term Frequency per document. So [{'hi': 1}] means
        the first document contains the term 'hi' 1 time.

    df_ : dict[str, int]
        Document Frequency per term. i.e. Number of documents in the
        corpus that contains the term.

    idf_ : dict[str, float]
        Inverse Document Frequency per term.

    doc_len_ : list[int]
        Number of terms per document. So [3] means the first
        document contains 3 terms.

    corpus_ : list[list[str]]
        The input corpus.

    corpus_size_ : int
        Number of documents in the corpus.

    avg_doc_len_ : float
        Average number of terms for documents in the corpus.
    """

    def __init__(self, k1=1.5, b=0.75):
        self.b = b
        self.k1 = k1

    def fit(self, corpus):
        """
        Fit the various statistics that are required to calculate BM25 ranking
        score using the corpus given.

        Parameters
        ----------
        corpus : list[list[str]]
            Each element in the list represents a document, and each document
            is a list of the terms.

        Returns
        -------
        self
        """
        tf = []
        df = {}
        idf = {}
        doc_len = []
        corpus_size = 0
        for document in corpus:
            corpus_size += 1
            doc_len.append(len(document))

            # compute tf (term frequency) per document
            frequencies = {}
            for term in document:
                term_count = frequencies.get(term, 0) + 1
                frequencies[term] = term_count

            tf.append(frequencies)

            # compute df (document frequency) per term
            for term, _ in frequencies.items():
                df_count = df.get(term, 0) + 1
                df[term] = df_count

        for term, freq in df.items():
            idf[term] = math.log(1 + (corpus_size - freq + 0.5) / (freq + 0.5))

        self.tf_ = tf
        self.df_ = df
        self.idf_ = idf
        self.doc_len_ = doc_len
        self.corpus_ = corpus
        self.corpus_size_ = corpus_size
        self.avg_doc_len_ = sum(doc_len) / corpus_size
        return self

    def search(self, query):
        scores = [self._score(query, index) for index in range(self.corpus_size_)]
        return scores

    def _score(self, query, index):
        score = 0.0

        doc_len = self.doc_len_[index]
        frequencies = self.tf_[index]
        for term in query:
            if term not in frequencies:
                continue

            freq = frequencies[term]
            numerator = self.idf_[term] * freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len_)
            score += (numerator / denominator)

        return score
