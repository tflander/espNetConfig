import pytest
from config import Config


def test_dictToJson():
    c = Config(ssid="foo", password="bar")
    configStr = c.asJson()
    assert configStr == '{"ssid": "foo", "password": "bar"}'


def test_readFile(tmpdir):

    fileName = tmpdir / "hello.txt"
    createConfigFile(fileName, ssid="foo", password="bar")
    c = Config.read(fileName)
    assert c.ssid == "foo"
    assert c.password == "bar"


def createConfigFile(file, ssid="foo", password="bar"):
    c = Config(ssid=ssid, password=password)
    configStr = c.asJson()
    f = file.open('w')
    f.write(configStr)
    f.close()
