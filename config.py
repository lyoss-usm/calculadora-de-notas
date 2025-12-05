import utils as ut

class Config:
    def __init__(self, config_file='data/config.json'):
        self.config = ut.read_json(config_file)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        ut.write_json(self.config, 'config.json')

    def __str__(self):
        return str(self.config)