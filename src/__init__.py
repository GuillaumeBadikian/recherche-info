import os
import time
from collections import namedtuple

from config.Config import Config
from src import rank
from src.compare import Compare
from src.parser.xml_parser import XmlsParser
from src.rank import Run, XmlRank
if __name__ == '__main__':

    conf = Config()

    k= 0.8
    b=0.4
    conf.setOthers(['k'+str(k), 'b'+str(b)])
    config = conf.getConfig()
    config = namedtuple("Conf", config['run'].keys())(*config['run'].values())

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
    file = ""
    for q in query:
        r = rank.getBm25(q[1],k=k,b=b)
        run = Run("".join(config.staff), config.step, config.num,config.weighting, config.granularity,config.others)
        file = run.createRun("../runs", r, q[0])
    conf.incrementRun()

    files = ["../runs/runs/15-12-2020/GuillaumeBenoitGauthierTheo_02_07_bm25_articles_k0.8_b0.4.txt",
             file]
    compare = Compare();
    df = compare.compare(files[0], files[1], 7, 20)
    print(df.to_string(max_rows=1000))
