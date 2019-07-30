import json

class Config:

    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.exists = True

    def asJson(self):
        return json.dumps({"ssid": self.ssid, "password": self.password})

    @classmethod
    def read(cls, filename):
        try:
            f = open(filename)
        except OSError:
            c = Config('', '')
            c.exists = False
            return c
        configDictionary = json.loads(f.read())
        f.close()
        return Config(configDictionary.get('ssid'), configDictionary.get('password'))

    def write(self, filename):
        f = open(filename, "w")
        f.write(self.asJson())
        f.close()
