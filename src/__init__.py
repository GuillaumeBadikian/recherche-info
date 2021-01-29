import importlib
import json
import os
import time
from collections import namedtuple

import pandas
import yaml

from config.Config import Config
from src import rank
from src.compare import Compare
from src.parser.xml_parser import XmlsParser
import matplotlib.pyplot as plt

from src.rank import *
from src.rank.rank import XmlRank
from src.run.run import Run


class Main:
    def __init__(self):

        conf = Config()

        config = conf.getConfig()
        config = namedtuple("Conf", config['run'].keys())(*config['run'].values())

        conf.setOthers(['k' + str(config.k), 'b' + str(config.b)])

        t = time.time()
        parser = XmlsParser("../data/coll")
        parser.parse()
        with open("./data.json", "w") as fi:
        #    yaml.dump(parser.corpusWcount, ymlfile)
        #ymlfile.close()
            json.dump(parser.corpusWcount,fi)
        #print(time.time()-t)
        rank = XmlRank(parser.corpusWcount)
        query = [
            [2009011, ["olive", "oil", "health"]],
            [2009036, ["notting", "hill", "film", "actors"]],
            [2009067, ["probabilistic", "models", "in", "information", "retrieval"]],
            [2009073, ["web", "link", "network", "analysis"]],
            [2009074, ["web", "ranking", "scoring", "algorithm"]],
            [2009078, ["supervised", "machine", "learning", "algorithm"]],
            [2009085, ["operating", "system", "mutual", "exclusion"]]

        ]
        file = ""
        func = getattr(importlib.import_module("src.rank"), config.weighting)
        for q in query:
            r = rank.getBm25(request=q[1],func=func, k=config.k,b=config.b,d=0)
            run = Run("".join(config.staff), config.step, config.num,config.weighting, config.granularity,config.others)
            file = run.createRun("../runs", r, q[0])
        conf.incrementRun()

        files = ["../runs/{}".format(config.compare),
                 file]
        compare = Compare()
        df = compare.compare(files[0], files[1], 7, 20)
        df.style.apply(lambda i : 'color : red' if i < 0 else 'color : green', subset=['diff'])
        print(df.to_string(max_rows=1000))



        #df.plot(use_index=True,y='diff', kind="line")
        fig, axes = plt.subplots(nrows=2, ncols=2)
        df.plot(use_index=True,y=['pos2'], kind="line", ax=axes[0,0])
        axes[0, 0].legend(['file 2'])
        df.plot(use_index=True,y=['pos2','pos'], kind="line", ax=axes[0,1])
        axes[0, 1].legend(['file 2', 'file'])
        df.plot(use_index=True,y=['diff'], kind="line", ax=axes[1,0])
        axes[1, 0].legend(['difference'])
        df.plot(use_index=True,y=['pos','pos2'], kind="density", ax=axes[1,1])
        axes[1, 1].legend(['file 1','file 2'])
        #plt.xlim(-50, 50)
        plt.xticks(rotation=65)
        plt.show()
        ax = plt.axes(projection='3d')
        zline = df['diff'].tolist()
        xline = df['pos2'].tolist()
        yline = df['pos'].tolist()
        ax.set_xlabel('diff')
        ax.set_ylabel('file 1')
        ax.set_zlabel('file 2')
        ax.scatter3D(xline, yline, zline)
        plt.show()



