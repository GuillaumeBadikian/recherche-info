from rank_bm25 import *

import src.rank.bm25  as bm1


def bm25(corpus, req, k, b, d):
    bm = bm1.BM25(k1=k, b=b)
    bm.fit(corpus)
    return bm.search(req)


def bm25l(corpus, req, k, b, d):
    bm = BM25L(corpus=corpus, k1=k, b=b, delta=d)
    return bm.get_scores(req)


def bm25plus(corpus, req, k, b, d):
    bm = BM25Plus(corpus=corpus, k1=k, b=b, delta=d)
    return bm.get_scores(req)


def bm25t(corpus, req, k, b, d):
    bm = bm1.BM25T(corpus, k1=k, b=b, delta=d)
    return bm.get_scores(req)


def bm25adpt(corpus, req, k, b, d):
    bm = bm1.BM25Adpt(corpus, k1=k, b=b, delta=d)
    return bm.get_scores(req)
