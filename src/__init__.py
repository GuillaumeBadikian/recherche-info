#!/usr/bin/python

import time

import nltk
from nltk import WordNetLemmatizer

from src.Compare import Compare
from src.Parser import Parser
import pandas as pd

from src.ParserXml import ParserXmls, ParserXmls
from xml.etree  import ElementTree

if __name__ == '__main__':
    #xmlParser = ParserXml()
    #tree = xml.parse('./data/coll/612.xml',xml.XMLParser)
    #tree = ET.parse('C:/Users/guill/Documents/fac\master/2A/RI/recherche-info/src/data/coll/612.xml')
    #parser.entity = AllEntities()
    '''parser = ElementTree.XMLParser()
    parser.entity['nbsp'] = " "
    #parser.parser.UseForeignDTD(True)

    tree = ElementTree.parse(source='./data/coll/612.xml', parser=parser)

    print(tree.getroot())'''
    '''comp = Compare()
    comp.compare("./runs/GuillaumeBenoitGauthierTheo_02_07_ltn_articles_.txt", "./runs/GuillaumeBenoitGauthierTheo_02_08_ltn_articles_.txt")'''
    start = time.time()
    corpus = ParserXmls("./data/coll")
    corpus.parse(verbose=True)
    print("time execution create vector {}".format(time.time() - start))
    start = time.time()
    corpus.createVector()
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

    corpus.scoreAndGenerate("GuillaumeBenoitGauthierTheo", "02", "03", "ltn", "articles", "lem",
                            search, search2, search3, search4, search5, search6, search7)

    print("time execution generate runs {}".format(time.time() - start))
    try:
        with open("./data/Text_Only_Ascii_Coll_MWI_NoSem", "r") as f:
            pass


            '''start = time.time()
            parser = Parser()
            parser.parse(f)
            print("time execution parsing {}".format(time.time() - start))

            start = time.time()
            parser.createVector()
            print("time execution create vector {}".format(time.time() - start))
            start = time.time()

            search = {2009011: ["olive", "oil", "health", "benefit"]}
            search2 = {2009036: ["notting", "hill", "film", "actors"]}
            search3 = {2009067: [ "probabilistic", "models", "in", "information", "retrieval"]}
            search4 = {2009073: ["web", "link","network","analysis"]}
            search5 = {2009074: ["web", "ranking","scoring","algorithm"]}
            search6 = {2009078: ["supervised", "machine","learning","algorithm"]}
            search7 = {2009085: ["operating", "system","+mutual","exclusion"]}

            parser.scoreAndGenerate("GuillaumeBenoitGauthierTheo", "01", "06", "ltn", "articles", "",
                    search, search2,search3,search4,search5,search6,search7)

            print("time execution generate runs {}".format(time.time() - start))'''

    except:
        print("error")
