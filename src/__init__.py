
import time
from src.Parsing import Parsing
from src.test import VectorModel

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
        #print(p.getWeight("10003934",w))
        print("time execution {}".format(time.time()-start))
        start = time.time()
        v = VectorModel(p)
        #v.createVector()
        #v.toJson("test")
        v.fromJson("./data/data.json")
        print("time execution {}".format(time.time() - start))
        print(v.vectorModel)
    #[print(i) for i in r]





