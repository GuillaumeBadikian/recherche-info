import importlib

from config.Config import Config
from src import Compare
from src.rank import *
import src.rank as a

if __name__ == '__main__':
    conf = Config()
    #full_module_name = "src.rank." + "mymodule"
    #getattr(a+".bm25L", "bm25L")()

    #mymethod = getattr(importlib.import_module("src.rank"), "bm25plus")
    #mymethod(["bf","f"],["re","t"],1,0.5,1)

    '''f = open("../runs/2021-01-23/GuillaumeBenoitGauthierTheo_06_18_bm25_element_k0.6_b0.3.txt")
    buff = f.readlines()
    res = dict()
    for i,b in enumerate(buff[:1500]):
        id = int(b.split()[2])
        if res.get(id) is not None:
            res[id].append(i)
        else:
            res[id] = [i]
    [print(i, j, len(j)>1)  for i,j in res.items() ]'''

    comp = Compare()

    df = comp.compare("../runs/2021-01-23/GuillaumeBenoitGauthierTheo_08_02_bm25_element_k0.3_b0.3.txt",
                 "../runs/2021-01-23/GuillaumeBenoitGauthierTheo_08_11_bm25_articles_k0.3_b0.3.txt",7,20)
    print(df.to_string(max_rows=1000))
