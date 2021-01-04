import yaml


class Config(object):
    class __Config:
        def __init__(self):
            self.confFile = "../config/conf.yml"

        def getConfig(self):
            with open(self.confFile, "r") as ymlfile:
                cfg = yaml.load(ymlfile.read(), Loader=yaml.FullLoader)
            return cfg

        def incrementRun(self):
            conf = self.getConfig()
            with open(self.confFile, "w") as ymlfile:
                conf['run']['num'] = conf['run']['num'] + 1
                yaml.dump(conf, ymlfile)

        def setOthers(self, others):
            conf = self.getConfig()
            with open(self.confFile, "w") as ymlfile:
                conf['run']['others'] = others
                yaml.dump(conf, ymlfile)

        def setConfig(self, conf):
            with open(self.confFile, "w") as ymlfile:
                yaml.dump(conf, ymlfile)
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
