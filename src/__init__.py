#!/usr/bin/python

import time
from src.Parsing import Parsing
from src import ranking
from src.ranking import score, generateRuns


if __name__ == '__main__':
    #nltk.download('stopwords')
    search = b"<doc>"
    result = []
    r = []

    start = time.time()
    with open("./data/Text_Only_Ascii_Coll_MWI_NoSem","r") as f:
        p = Parsing()
        p.parse(f)
        w = "States"
        print("time execution {}".format(time.time() - start))
        print(p.getTf("10003934", w))
        print(p.getIdf(w))
        print(p.getWeight("10003934",w))
        print("time execution {}".format(time.time()-start))
    #[print(i) for i in r]



