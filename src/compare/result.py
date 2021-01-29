import glob

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

class Result:
    def __init__(self, dir):
        self.dir = dir
        self.infos = dict()
        self.__load()

    def __load(self):
        files = glob.glob(self.dir + "/*.txt")
        for fi in files:
            f = open(fi, "r")
            buff = f.readlines()[1:-1]
            fn = dict()
            for b in buff:
                a = b.split()
                # print(a[1])
                fn[a[0]] = (a[1], a[2])
                # print(b.split())
            self.infos[fi] = fn

    def compareLine(self, line, filter=None):
        res = []
        ind = []
        for (k,v) in self.infos.items():
            for (w,x) in v.items():
                if w==line:
                    info = k.split("_")
                    if(info[1]=="res\GuillaumeBenoitGauthierTheo"):
                        res.append({'name' : str(info[1]), 'methods':info[4],'param': "_".join(info[5:]), line : float(x[1]) })
                        ind.append("_".join(info[1:]).replace(".i.txt"," ")+line)
                    #res.append({'name' : info[0] })
                    #print("_".join(k.split("_")[4:]),x[1])
        df = pd.DataFrame(res, columns=['name', 'methods', 'param', line], index=ind)
        if filter:
            return df.query(filter)
        return df
if __name__ == '__main__':
    dir = "../../data/rendu/rendu9_res"
    res = Result(dir)
    df = res.compareLine("MAgP","MAgP > 0.15")
    #print(df.sort_values(by=['MAgP']).to_string(max_cols=4,max_rows=1000))
    #print(df['name'])
    df2 = df.sort_values(by=['MAgP'])
    print(df2)
    fig, ax = plt.subplots()
    plt.barh(df2.index, df2['MAgP'] )
    plt.yticks(fontsize=5)
    plt.axvline(x=0.2, color='red', linestyle='--', linewidth=1)

    plt.show()