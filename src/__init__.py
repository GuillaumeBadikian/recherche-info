#!/usr/bin/python

import time
from src.Parser import Parser
import pandas as pd

if __name__ == '__main__':
    #nltk.download('stopwords')
    search = b"<doc>"
    result = []
    r = []

    start = time.time()
    with open("./data/Text_Only_Ascii_Coll_MWI_NoSem","r") as f:

        start = time.time()
        parser = Parser()
        parser.parse(f)
        print("time execution parsing {}".format(time.time() - start))
        start = time.time()
        parser.createVector()
        print("time execution create vector {}".format(time.time() - start))
        #parser.fromJson("./data/test.json")
        start = time.time()
        search = ["olive", "oil", "health", "benefit"]
        parser.score(search)
        parser.generateRuns(1456561,"guillaume")
        print("time execution generate runs {}".format(time.time() - start))
        #[print(t,u) for (t,u) in parser.vectorModel.items() if t[0]=="11735612"]
        #pd.DataFrame(parser.docParse)
        #print(pd.DataFrame(parser.getVectorModelList()))
        vector = parser.getVectorModelList()
        #df = pd.DataFrame(columns=parser.getDocsNo())
        #[print(i[0]) for i in vector]

    #[print(i) for i in r]





