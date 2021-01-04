import os
import time

from src2 import rank
from src2.compare import Compare
from src2.parser.xml_parser import XmlsParser
from src2.rank import Run, XmlRank

if __name__ == '__main__':

    num_run = "17"
    staff = "GuillaumeBenoitGauthierTheo"
    step = "04"
    weighting = "bm25"
    granularity = "articles"
    others = ["k0.8","b0.4"]
    t = time.time()
    parser = XmlsParser("../data/coll")
    parser.parse()
    #print(time.time()-t)
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
        r = rank.getBm25(q[1],k=0.8,b=0.4)
        run = Run(staff, step, num_run,weighting, granularity,others)
        run.createRun("../runs", r, q[0])

    files = ["../runs/2021-01-04/GuillaumeBenoitGauthierTheo_04_16_bm25_articles_k0.8_b0.4.txt",
             "../src/runs/15-12-2020/GuillaumeBenoitGauthierTheo_02_07_bm25_articles_k0.8_b0.4.txt"]
    compare = Compare();
    df = compare.compare(files[0], files[1], 7, 20)
    print(df.to_string(max_rows=1000))
