import yaml


class Configuration:
    def __init__(self, path):
        self.config = {}
        with open(path) as c:
            self.config = yaml.load(c, Loader=yaml.FullLoader)

    def __getitem__(self, key):
        return self.config.get(key)

    def __repr__(self):
        return str(self.config)