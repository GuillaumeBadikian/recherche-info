import rank_bm25
from nltk.corpus import stopwords

from src import Compare, Parser
from src.rank import XmlRank, Run, BM25
from src.xml_parser import XmlsParser, XmlParser


def testXml():
    stop_words = set(stopwords.words("english"))
    corpus = dict()
    corpusW = dict()
    parser = XmlParser("../src/data/coll/3951433.xml", stop_words, "[\w'/():\"@+-]*", corpus, corpusW)
    parser.run()
    print(len(parser.corpusWcount['3951433']))
    parser2 = XmlParser("../src/data/coll/22478.xml", stop_words, "[\w'/():\"@+-]*", corpus, corpusW)
    parser2.run()
    print(len(parser.corpusWcount['22478']))


    bm25 = rank_bm25.BM25L([parser.corpusWcount['3951433'], parser2.corpusWcount['22478']], k1=1.2, b=0.75)
    doc_scores = bm25.get_scores(["olive", "oil", "health", "benefit"])
    print(doc_scores)

    bm25 = rank_bm25.BM25Okapi([parser.corpusWcount['3951433'], parser2.corpusWcount['22478']], k1=1.2, b=0.75)
    doc_scores = bm25.get_scores(["olive", "oil", "health", "benefit"])
    print(doc_scores)

    bm25 = rank_bm25.BM25Plus([parser.corpusWcount['3951433'], parser2.corpusWcount['22478']], k1=1.2, b=0.75)
    doc_scores = bm25.get_scores(["olive", "oil", "health", "benefit"])
    print(doc_scores)

    bm25 = BM25()
    bm25.fit([parser.corpusWcount['3951433'], parser2.corpusWcount['22478']])
    doc_scores = bm25.search(["olive", "oil", "health", "benefit"])
    print(doc_scores)

def parse():
    parser = XmlsParser("../src/data/coll")
    parser.parse()
    return parser
    # print(parser.corpus)
    print("rank")
    #[print(i, len(j)) for i, j in parser.corpusWcount.items()]

def rank(parser,re):
    rank = XmlRank(parser.corpusWcount)
    query = [2009011, ["olive", "oil", "health"]]

    r = rank.getBm25(query[1])
    run = Run("GuillaumeBenoitGauthierTheo", "02", re, "ltn", "articles", ["sem", "test"])
    run.createRun("../src/runs", r, query[0])

def comp(re):
    comp = Compare()
    files = ["../src/runs/10-12-2020/EliasNicolas_01_04_bm25_articles_k0.5b0.3.txt",
             "../src/runs/11-12-2020/GuillaumeBenoitGauthierTheo_02_"+re+"_ltn_articles_sem_test.txt"]
    df = comp.compare(files[0], files[1], 7, 50)
    print(df[:40])


def run(re):
    parser = parse()
    rank(parser, re)
    comp(re)


def run2(re):
    with open("../src/data/Text_Only_Ascii_Coll_MWI_NoSem", "r") as f:
        parser = Parser()
        parser.parse(f)
        #print(parser.corpusW)
        #[print(i,j) for i,j in parser.corpusW.items()]
        parser.createVector()

        search = {2009011: ["olive", "oil", "health", "benefit"]}
        search2 = {2009036: ["notting", "hill", "film", "actors"]}
        search3 = {2009067: ["probabilistic", "models", "in", "information", "retrieval"]}
        search4 = {2009073: ["web", "link", "network", "analysis"]}
        search5 = {2009074: ["web", "ranking", "scoring", "algorithm"]}
        search6 = {2009078: ["supervised", "machine", "learning", "algorithm"]}
        search7 = {2009085: ["operating", "system", "+mutual", "exclusion"]}
        parser.scoreAndGenerate("GuillaumeBenoitGauthierTheo", "02", re, "ltn", "articles", "sem_test",
                                search, search2, search3, search4, search5, search6, search7)

if __name__ == '__main__':
    re = "202"
    #run(re)
    comp(re)
    #testXml()
