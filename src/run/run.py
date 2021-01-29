import os
from datetime import date

from colorama import Fore
from src.run import numberToString

class Run():
    def __init__(self, staff, step, run, weightingF, granularity, others=[]):
        self.staff = staff
        self.step = step
        self.run = run
        self.weightingFunc = weightingF
        self.granularity = granularity
        self.others = others

    def createRun(self, dir, ranking, queryId, limit=1500, verbose = True, elem=None):
        d = "{}/{}".format(dir, date.today().strftime("%Y-%m-%d"))
        if not os.path.exists(d):
            os.makedirs(d)
        if verbose:
            print("{}Drafting of the classification of the request id {} {} {} in file:///{}/{} {}".format(
                Fore.CYAN,Fore.GREEN,queryId, Fore.CYAN,
                os.path.abspath(d).replace("\\", "/"),self.getFormat(), Fore.RESET))
        f = open("{}/{}".format(d, self.getFormat()), 'a')
        rank = 1
        runs = ""
        path = "/article[1]" if elem is None else elem
        for r in ranking:
            #if rank > limit: break
            current_run = f'{queryId} {numberToString(self.step)} {r[0]} {rank} {str(r[1])} {self.staff} {path}'
            runs += current_run + "\n"
            rank += 1

        f.write(runs)
        f.close()
        return "{}/{}".format(d, self.getFormat())

    def createRunElem(self, dir, ranking, queryId, limit=1500, verbose = True):
        d = "{}/{}".format(dir, date.today().strftime("%Y-%m-%d"))
        if not os.path.exists(d):
            os.makedirs(d)
        if verbose:
            print("{}Drafting of the classification of the request id {} {} {} in file:///{}/{} {}".format(
                Fore.CYAN, Fore.GREEN, queryId, Fore.CYAN,
                os.path.abspath(d).replace("\\", "/"), self.getFormat(), Fore.RESET))
        f = open("{}/{}".format(d, self.getFormat()), 'a')
        rank = 1
        runs = ""
        #path = "/article[1]" if elem is None else elem
        for r in ranking:
            #if rank > limit: break
            current_run = f'{queryId} {numberToString(self.step)} {str(r[0])} {rank} {str(r[2])} {self.staff} {r[1]}'
            runs += current_run + "\n"
            rank += 1

        f.write(runs)
        f.close()
        return "{}/{}".format(d, self.getFormat())

    def getFormat(self):
        return "{}_{}_{}_{}_{}_{}.txt".format(self.staff, numberToString(self.step), numberToString(self.run), self.weightingFunc, self.granularity,
                                              '_'.join(self.others))


