import os
from collections import namedtuple

from config.Config import Config
from src.main import Main

if __name__ == '__main__':
    os.chdir(os.getcwd() + "/src/")
    config = Config().getConfig()
    query = []
    for q in config['query']:
        query.append([list(q.keys())[0],list(q.values())[0]])
    main = Main()
    main.load()
    config = namedtuple("Conf", config['run'].keys())(*config['run'].values())

    if config.granularity == "articles":
        main.rank_article(query)
    else:
        main.rank_elem(query)

