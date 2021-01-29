import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


class Compare:

    def __init__(self):
        self.df = None

    def compare(self, file, file2, req, inf):
        inf = inf - 2
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
            # i += t * 1500 - t * inf
            i = t * 1500 + j
            for l2 in buff2:
                if buff[i].split(" ")[2] == l2.split(" ")[2]:
                    doc1 = [buff[i].split(" ")[2], buff[i].split(" ")[3]]
                    doc2 = [l2.split(" ")[2], l2.split(" ")[3]]
                    diff = int(l2.split(" ")[3]) - int(buff[i].split(" ")[3])
                    res.append({'doc1': int(doc1[0]), 'pos': int(doc1[1]), 'doc2': int(doc2[0]), 'pos2': int(doc2[1]),
                                'diff': diff})
                    hasres = True
                    break
            # if not hasres:
            #    res.append({'doc1':buff[i].split(" ")[2], 'pos': buff[i].split(" ")[3], 'doc2': 'unknown', 'pos2': 'unknown', 'diff': 'unknown'})
            j += 1
            if i > (inf + (t * 1500)):
                t += 1
                j = 0

        self.df = pd.DataFrame(res, columns=['doc1', 'pos', 'doc2', 'pos2', 'diff'])

        return self.df


class CompareTo:

    def __init__(self, file, file2):
        self.file = file
        self.file2 = file2
        '''@:type DataFrame'''
        self.df = None

    def compare(self, req):
        header = ["req", "step", "docid", "rank", "score", "staff", "granu"]
        df1 = pd.read_csv(self.file, sep=" ", header=None, names=header).query('req == {}'.format(req))
        df2 = pd.read_csv(self.file2, sep=" ", header=None,
                          names=["req", "step2", "docid", "rank2", "score2", "staff2", "granu2"]) \
            .query('req == {}'.format(req))
        df3 = pd.merge(df1, df2, on="docid", how='left')

        self.df = df3
        return df3[['docid', 'rank', "rank2"]]

    def show(self, nb=50):
        fig, axes = plt.subplots(nrows=1, ncols=1)
        df = self.df[['docid', 'rank', "rank2"]]
        df = df.assign( Diff=df['rank'] - df['rank2'])
        df[:nb].plot.bar(x="docid", y=["Diff"], rot=0, title='difference between runs articles with different tokenization')
        #df[:nb].plot.bar(x="Diff", y=["rank2", "rank"], rot=0)
        plt.xticks(rotation=65)
        plt.show()



if __name__ == '__main__':
    comp = CompareTo("../../runs/2021-01-08/GuillaumeBenoitGauthierTheo_04_85_bm25_articles_k0.8_b0.4.txt",
                     "../../runs/2021-01-16/GuillaumeBenoitGauthierTheo_06_82_bm25_articles_k0.8_b0.4.txt")

    comp.compare(2009011)
    comp.show()
