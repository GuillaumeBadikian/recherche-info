import sys

import yaml


class Config(object):
    class __Config:
        def __init__(self):
            self.confFile = "../config/conf.yml"

        def getConfig(self):
            try:
                with open(self.confFile, "r") as ymlfile:
                    cfg = yaml.load(ymlfile.read(), Loader=yaml.FullLoader)
                ymlfile.close()
                return cfg
            except:
                sys.stderr.write("file {} not found".format(self.confFile))
                exit(-1)

        def incrementRun(self):
            conf = self.getConfig()
            with open(self.confFile, "w") as ymlfile:
                conf['run']['num'] = conf['run']['num'] + 1
                yaml.dump(conf, ymlfile)
            ymlfile.close()

        def setOthers(self, others):
            conf = self.getConfig()
            with open(self.confFile, "w") as ymlfile:
                conf['run']['others'] = others
                yaml.dump(conf, ymlfile)
            ymlfile.close()

        def setConfig(self, conf):
            with open(self.confFile, "w") as ymlfile:
                yaml.dump(conf, ymlfile)
            ymlfile.close()
            return self

    instance = None

    def __new__(self):
        if not Config.instance:
            Config.instance = Config.__Config()
        return Config.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
