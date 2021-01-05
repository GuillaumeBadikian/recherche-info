import importlib

from config.Config import Config
from src.rank import *
import src.rank as a

if __name__ == '__main__':
    conf = Config()
    #full_module_name = "src.rank." + "mymodule"
    #getattr(a+".bm25L", "bm25L")()

    mymethod = getattr(importlib.import_module("src.rank"), "bm25plus")
    mymethod(["bf","f"],["re","t"],1,0.5,1)

