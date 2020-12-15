#!/usr/bin/python

import time

import nltk
import pytest
from nltk import WordNetLemmatizer

from src.Compare import Compare
import pandas as pd

from src.ParserXml import ParserXmls, ParserXmls
from xml.etree  import ElementTree

from src.rank import XmlRank, Run
from src.xml_parser import XmlsParser
from test import Test

def run():
    nb_run = "10"
    parser = XmlsParser("../src/data/coll")
    parser.parse()
    rank = XmlRank(parser.corpusWcount)
    query = [
        [2009011, ["olive", "oil", "health"]],
        [2009036, ["notting", "hill", "film", "actors"]],
        [2009067, ["probabilistic", "models", "in", "information", "retrieval"]],
        [2009073, ["web", "link", "network", "analysis"]],
        [2009074, ["web", "ranking", "scoring", "algorithm"]],
        [2009078, ["supervised", "machine", "learning", "algorithm"]],
        [2009085, ["operating", "system", "+mutual", "exclusion"]]

    ]

    for q in query:
        r = rank.getBm25(q[1])
        run = Run("GuillaumeBenoitGauthierTheo", "02", nb_run, "bm25", "articles", ["k1.2","b0.4"])
        run.createRun("../src/runs", r, q[0])


if __name__ == '__main__':

    start = time.time()
    #run()
    print(time.time()-start)

    files = ["runs/15-12-2020/GuillaumeBenoitGauthierTheo_02_03_ltn_articles.txt",
             "runs/15-12-2020/GuillaumeBenoitGauthierTheo_02_04_ltn_articles.txt"]
    compare = Compare();
    df = compare.compare(files[0], files[1], 7, 50)
    print(df[:40])
