import json
import time
import copy

from src import Compare, ParserXmls, Parser


class Test:

    def ltnSem(self):
        start = time.time()
        corpus = ParserXmls("./data/coll")
        cor = corpus.parse(verbose=True)
        print("time execution create vector {}".format(time.time() - start))
        start = time.time()
        #corpus.createVector()
        corpus.bm25(cor)
        print("time execution create vector {}".format(time.time() - start))
        start = time.time()
        corpus.toJson("./data/lem.json")
        search = {2009011: ["olive", "oil", "health", "benefit"]}
        search2 = {2009036: ["notting", "hill", "film", "actors"]}
        search3 = {2009067: ["probabilistic", "models", "in", "information", "retrieval"]}
        search4 = {2009073: ["web", "link", "network", "analysis"]}
        search5 = {2009074: ["web", "ranking", "scoring", "algorithm"]}
        search6 = {2009078: ["supervised", "machine", "learning", "algorithm"]}
        search7 = {2009085: ["operating", "system", "+mutual", "exclusion"]}

        corpus.scoreAndGenerate("GuillaumeBenoitGauthierTheo", "02", "103", "ltn", "articles", "sem_test",
                                search, search2, search3, search4, search5, search6, search7)


        print("time execution generate runs {}".format(time.time() - start))

    def compare(self, f1, f2, req, inf):
        comp = Compare()
        df = comp.compare(f1, f2, req, inf)
        print(df[:40])
        print(df[40:65])

    def txt_ltn(self, step, req_n):
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
            search3 = {2009067: ["probabilistic", "models", "in", "information", "retrieval"]}
            search4 = {2009073: ["web", "link", "network", "analysis"]}
            search5 = {2009074: ["web", "ranking", "scoring", "algorithm"]}
            search6 = {2009078: ["supervised", "machine", "learning", "algorithm"]}
            search7 = {2009085: ["operating", "system", "+mutual", "exclusion"]}

            parser.scoreAndGenerate("GuillaumeBenoitGauthierTheo", step, req_n, "ltn", "articles", "test",
                                    search, search2, search3, search4, search5, search6, search7)

            print("time execution generate runs {}".format(time.time() - start))

    def testParse(self):
        parser = Elem.Elem()
        doc = parser.xmltodict2("./data/coll/10003934.xml")
        l = self.par(doc)
        t = " ".join(l)
        print(len(t.split(" ")))
        # print(doc['article']['entity']['bdy']['table']['row'][0]['header']['supreme_court']['link'])
        # parser.iterdict(doc)

    def parcoursList(self, l):
        for i in l:
            self.parcours(i)

    def parcours(self, doc):

        for k in doc:
            print(k, isinstance(doc[k][0], list))
            print(isinstance(doc[k][0], dict))

    def par(self, doc):
        l = []
        self.te(doc, l)

        # t = (" ".join(l).split())
        return l

    def te(self, doc, l):
        if isinstance(doc, dict):
            for (k, v) in doc.items():
                self.te(v, l)
                '''if isinstance(doc[k],list):
                    for i in doc[k]:
                        self.te(i)'''

        elif isinstance(doc, list):
            for i in doc:
                self.te(i, l)

        elif isinstance(doc, str):
            l.append(doc)
        else:
            pass  # print(type(doc))

    def test2(self):
        parser = Elem.Elem()
        doc = parser.xmltodict2("./data/coll/10003934.xml")
        #print(doc['article'][0]['entity'][0]['header'][0]['id'][0])
        #print("test")
        l2 = self.search(doc,"id")
        print(l2)

    def parc(self, doc):
        l1 = []
        self.parc2(doc, l1)
        return " ".join(l1)

    def parc2(self, doc, l):
        if isinstance(doc, dict):
            for (k, v) in doc.items():
                self.parc2(v,l)
        elif isinstance(doc, list):
            for i in doc:
                self.parc2(i,l)

        elif isinstance(doc, str):
            l.append(doc)
        return l

    def search2(self, st, w, p, q):
        """
        search recursively a string into a Dict : Key or Value
        :param st: String to search
        :param w: Dict where search
        :param p: List of string of n-1 path into Dict (overTree)
        :param q: List of string which contains path where st has been found
        :return: List of path where st found
        """
        if isinstance(w, list):
            for a, i in enumerate(w,0):
                if(isinstance(i,dict) or isinstance(i,list)):
                    p.append(a)
                self.search2(st, i, p, q)

        elif isinstance(w, dict):
            for (k, v) in w.items():
                if k == st or v == st:
                    #q.append(copy.deepcopy(p))
                    q.append(v[0])
                p.append(k)
                self.search2(st, v, p, q)
                p.remove(k)  # rm sub trees when up


        return q

    def search(self, doc, st):
        """
        :param st: string to search
        :return: List of path where st found
        """
        t = []
        q = []
        w = doc
        self.search2(st, w, t, q)
        return q


