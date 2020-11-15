#!/usr/bin/python

import time
from src.Parser import Parser
import pandas as pd

if __name__ == '__main__':
    # nltk.download('stopwords')
    try:
        with open("./data/Text_Only_Ascii_Coll_MWI_NoSem", "r") as f:

            start = time.time()
            parser = Parser()
            parser.parse(f)
            print("time execution parsing {}".format(time.time() - start))

            start = time.time()
            parser.createVector()
            print("time execution create vector {}".format(time.time() - start))
            start = time.time()

            search = {2009011: ["olive", "oil", "health", "benefit"]}
            search2 = {2009036: ["notting", "hill", "film", "actors"]}
            search3 = {2009067: [ "probabilistic", "models", "in", "information", "retrieval"]}
            search4 = {2009073: ["web", "link","network","analysis"]}
            search5 = {2009074: ["web", "ranking","scoring","algorithm"]}
            search6 = {2009078: ["supervised", "machine","learning","algorithm"]}
            search7 = {2009085: ["operating", "system","+mutual","exclusion"]}

            parser.scoreAndGenerate("GuillaumeBenoitGauthierTheo", "01", "04", "ltn", "articles", "",
                    search, search2,search3,search4,search5,search6,search7)

            print("time execution generate runs {}".format(time.time() - start))

    except:
        print("error")
