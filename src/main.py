import glob
import importlib
import json
from collections import namedtuple
from os import path

import nltk
import xmltodict
from colorama import Fore
from keras_preprocessing.text import text_to_word_sequence
from nltk.corpus import stopwords

from config.Config import Config
from src import XmlRank, Run
from src.parser import getFullText, search, clean_text



class Main:
    def __init__(self):
        self.conf = Config()
        #self.docs = []
        self.docs = dict()

    def createData(self):
        config = self.conf.getConfig()
        config = namedtuple("Conf", config['run'].keys())(*config['run'].values())
        xmlsf = "../{}/*.xml".format(config.data['path'])
        xmls = glob.glob(xmlsf)
        for (i,xml) in enumerate(xmls):
            e = self.elem(xml)
            self.docs.update(e)
            percent = i / len(xmls) * 100
            print("\r{}files reading : {} {}  {} {:3.2f}%".format(Fore.CYAN, Fore.BLUE, xml.ljust(30),
                                                                  Fore.RED if percent < 100 else Fore.LIGHTGREEN_EX,
                                                                  percent), end='')
        print("\r{}files reading : {} {}  {} {:3.2f}%".format(Fore.CYAN, Fore.BLUE, xml.ljust(30),
                                                              Fore.RED if percent < 100 else Fore.LIGHTGREEN_EX,
                                                              percent), end='')
        print(Fore.RESET)
        with open("../data/data.json", "w") as fi:
            json.dump(self.docs,fi)
        return self.docs

    def s(self, t, size=80):
        r = dict()
        stop_words = set(stopwords.words("english"))
        self.s_r(t, r, stop_words, size=size)
        return r

    def s_r(self, t, r,stop_words, size=80, node=None):
        if isinstance(t, dict):
            for (k, v) in t.items():
                for i, j in enumerate(v, 0):
                    words = text_to_word_sequence(clean_text(getFullText(j)))
                    words = [w.lower() for w in words if not w in stop_words and w != '' and w.isalpha() and len(w) > 1]
                    node = node if node!=None else "/"
                    if len(words) > size:
                        if k=="#text":
                            r[node] = words
                        else:
                            r["{}/{}[{}]".format(node,k, i+1)]  = words
                        self.s_r(j, r, stop_words, size, node="{}/{}[{}]".format(node,k,i+1))

        return r

    def elem(self,xml):

        config = self.conf.getConfig()
        config = namedtuple("Conf", config['run'].keys())(*config['run'].values())
        with open(xml, encoding="utf-8") as fd:
            tree = xmltodict.parse(fd.read(), xml_attribs=False, force_list=True)
            '''document = getFullText(tree)
            text = clean_text(document)
            words = text_to_word_sequence(text)'''
            ra = self.s(tree, 30)
            doc_id = search(tree, "id")[0]

            return {doc_id : ra}

    def load(self):
        config = self.conf.getConfig()
        dataf = "../{}".format(config['run']["data"]['file'])
        if not path.exists(dataf) or config['run']['data']['overwrite'] is True:
            self.createData()
        if len(self.docs) == 0:
            with open(dataf) as f:
                self.docs = json.load(f)

    def __articles(self,query) -> list:
        config = self.conf.getConfig()
        config = namedtuple("Conf", config['run'].keys())(*config['run'].values())
        req = dict()
        for (k, v) in self.docs.items():
            if '//article[1]' in v:
                req[k] = v['//article[1]']
        rank = XmlRank(req)
        bm = []
        func = getattr(importlib.import_module("src.rank"), config.weighting)

        for q in query:
            req = clean_text(" ".join(q[1])).split()
            r = rank.getBm25(request=req, func=func, k=config.k, b=config.b, d=1)
            bm.append((q,r[:config.limit]))
        return bm

    def rank_article(self, query):
        config = self.conf.getConfig()
        config = namedtuple("Conf", config['run'].keys())(*config['run'].values())
        articles = self.__articles(query)
        for i in articles :
            run = Run("".join(config.staff), config.step, config.num, config.weighting, config.granularity,
                      ['k' + str(config.k), 'b' + str(config.b)])
            file = run.createRun("../runs", i[1], i[0][0])

        self.conf.incrementRun()

    def rank_elem(self, query):
        config = self.conf.getConfig()
        config = namedtuple("Conf", config['run'].keys())(*config['run'].values())
        docsEl = dict()
        for (k, v) in self.docs.items():
            for (w,x) in v.items():
                key = (k+w)
                docsEl[key] = x

        rank = XmlRank(docsEl)
        bm = []
        func = getattr(importlib.import_module("src.rank"), config.weighting)
        for q in query:
            req = clean_text(" ".join(q[1])).split()
            r = rank.getBm25(request=req, func=func, k=config.k, b=config.b, d=0)
            red = dict()
            fres = []
            lid = 0
            for t in r:
                if (len(fres) == config.limit):
                    break
                id, res = t[0].split("/",1)
                if red.get(id) is None:
                    red[id] = [res]
                    fres.append((id,res,t[1]))
                    lid = id
                else:
                    rec = False
                    for z in red[id]:
                        if res in z or z in res:
                            rec = True
                    if not rec and id == lid:
                        red[id].append(res)
                        fres.append((id, res, t[1]))
                        lid = id

            run = Run("".join(config.staff), config.step, config.num, config.weighting, config.granularity,
                     ['k' + str(config.k), 'b' + str(config.b)])
            file = run.createRunElem("../runs", fres, q[0])

        self.conf.incrementRun()

