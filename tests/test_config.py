from config import Config


def test_readFile(tmpdir):

    fileName = tmpdir / "existingConfig.json"
    createConfigFile(fileName, ssid="foo", password="bar")
    c = Config.read(fileName)
    assert c.ssid == "foo"
    assert c.password == "bar"

def test_writeFile(tmpdir):
    fileName = tmpdir / "newConfig.json"
    newConfig = Config(ssid="foo", password="bar")
    newConfig.write(fileName)

    configFromFile = Config.read(fileName)
    assert configFromFile.ssid == "foo"
    assert configFromFile.password == "bar"

def createConfigFile(file, ssid, password):
    c = Config(ssid=ssid, password=password)
    configStr = c.asJson()
    f = file.open('w')
    f.write(configStr)
    f.close()
