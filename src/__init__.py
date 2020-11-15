#!/usr/bin/python

import time
from src.Parser import Parser
import pandas as pd

if __name__ == '__main__':
    #nltk.download('stopwords')
    search = b"<doc>"
    result = []
    r = []

    with open("./data/Text_Only_Ascii_Coll_MWI_NoSem","r") as f:

        start = time.time()
        parser = Parser()
        #parser.parse(f)
        print("time execution parsing {}".format(time.time() - start))
        start = time.time()
        #parser.createVector()
        print("time execution create vector {}".format(time.time() - start))
        parser.fromJson("./data/test.json")
        start = time.time()
        search = {2009011 : ["olive", "oil", "health", "benefit"]}
        search2 = {2009012 : ["az", "oil", "health", "benefit"]}
        #search2 = ["az", "oil", "health", "benefit"]
        #parser.scoreAndGenerate("01", "guillaume", "02", search, search2)
        parser.scoreAndGenerate("GuillaumeBenoit",1, 2,"ltn","articles","test",search,search2)
        #parser.score(search)
        #parser.generateRuns(1456561,"guillaume","Q0")
        print("time execution generate runs {}".format(time.time() - start))
        #[print(t,u) for (t,u) in parser.vectorModel.items() if t[0]=="11735612"]
        #pd.DataFrame(parser.docParse)
        #print(pd.DataFrame(parser.getVectorModelList()))
        vector = parser.getVectorModelList()
        #df = pd.DataFrame(columns=parser.getDocsNo())
        #[print(i[0]) for i in vector]

    #[print(i) for i in r]'''





