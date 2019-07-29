import json

class Config:

    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def asJson(self):
        return json.dumps({"ssid": self.ssid, "password": self.password})

    @classmethod
    def read(cls, filename):
        f = open(filename)
        x = f.read()
        f.close()
        foo = json.loads(x)
        return Config(foo.get('ssid'), foo.get('password'))
