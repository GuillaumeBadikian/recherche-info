
import pandas as pd


class Compare:

    def __init__(self):
        self.df = None


    def compare(self, file, file2, req, inf):
        inf = inf -2
        f = open(file)
        buff = f.readlines()
        f.close()
        f2 = open(file2)
        buff2 = f2.readlines()
        f2.close()
        res = []
        t = 0
        j = 0

        for i in range(len(buff)):
            hasres = False
            if t >= req:
                break
            #i += t * 1500 - t * inf
            i = t*1500 +j
            for l2 in buff2:
                if buff[i].split(" ")[2] == l2.split(" ")[2]:
                    doc1 = [buff[i].split(" ")[2],  buff[i].split(" ")[3]]
                    doc2 = [l2.split(" ")[2],  l2.split(" ")[3]]
                    diff = int(l2.split(" ")[3]) - int(buff[i].split(" ")[3])
                    res.append( {'doc1' : int(doc1[0]) , 'pos' : int(doc1[1]), 'doc2' : int(doc2[0]) , 'pos2' : int(doc2[1]), 'diff' : diff})
                    hasres = True
                    break
            #if not hasres:
            #    res.append({'doc1':buff[i].split(" ")[2], 'pos': buff[i].split(" ")[3], 'doc2': 'unknown', 'pos2': 'unknown', 'diff': 'unknown'})
            j += 1
            if i > (inf + (t * 1500)):
                t += 1
                j= 0



        self.df = pd.DataFrame(res, columns=['doc1','pos','doc2','pos2','diff'])

        return self.df
