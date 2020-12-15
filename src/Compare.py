import copy

import pandas as pd


class Compare():

    def __init__(self):
        self.df = None


    def compare(self, file, file2, req, inf):
        inf = inf-2
        f = open(file)
        buff = f.readlines()
        f.close()
        f2 = open(file2)
        buff2 = f2.readlines()
        f2.close()
        res = []
        t = 0
        # for (i, line) in enumerate(buff):
        for i in range(len(buff)):
            if t >= req:
                break
            i += t * 1498 - t *inf

            for l2 in buff2:
                if buff[i].split(" ")[2] == l2.split(" ")[2]:
                    doc1 = [buff[i].split(" ")[2],  buff[i].split(" ")[3]]
                    doc2 = [l2.split(" ")[2],  l2.split(" ")[3]]
                    diff = int(l2.split(" ")[3]) - int(buff[i].split(" ")[3])
                    res.append( {'doc1' : doc1[0] , 'pos' : doc1[1], 'doc2' : doc2[0] , 'pos2' : doc2[1], 'diff' : diff})
                    break
            if i > (inf + (t * 1500)):
                t += 1

        self.df = pd.DataFrame(res, columns=['doc1','pos','doc2','pos2','diff'])

        return self.df
