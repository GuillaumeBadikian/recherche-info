
'''vectorModel{
("doc1", "terme1"):  weight,
 ("doc1", "terme2"): 100
}'''
from src import Parsing
import json

class VectorModel:
    def __init__(self, corpus : Parsing):
        self.corpus = corpus
        self.vectorModel = dict()

    def createVector(self):
        w = 0
        for (i, j) in self.corpus.docParse.items():
            for (k, l) in j.items():
                self.vectorModel[(i, k)] = self.corpus.getWeight(i, k)
            w += 1

        return self.vectorModel


    def toJson(self, dest : str):
        if self.vectorModel != []:
            l = []
            for(i,j) in self.vectorModel.items():
                l.append([i[0],i[1],j])
            data = json.dumps(l)
            #print(data)
            with open(dest, 'w') as f:
                f.write(data)
    def fromJson(self,fr : str):
        with open(fr, 'r') as f:
            vector = json.load(f)
            for i in vector:
                self.vectorModel[(i[0],i[1])] = i[2]
        # {
        # docNo : { w : f } ,
        # docNo : { w : f } ,
        # docNo : { w : f } ,
        # docNo : { w : f } ,
        #}