import configHttpServer
import os.path
import machine


class TestHandleClientRequest:

    request = ['GET /?ssid=foo&password=bar HTTP/1.1\r\n']
    configServer = configHttpServer.ConfigHttpServer("fake server socket")

    def test_writes_config_file(self):

        self.configServer.handle_client_request(self.request, FakeClientSocket())

        assert os.path.exists("config.json")
        f=open("config.json")
        assert f.read() == '{"ssid": "foo", "password": "bar"}'
        os.remove("config.json")

    def test_exits_if_empty_request(self):
        empty_request = ['GET ']
        self.configServer.handle_client_request(empty_request, FakeClientSocket())
        assert not os.path.exists("config.json")

    def test_reboots_device(self):
        self.configServer.handle_client_request(self.request, FakeClientSocket())
        assert machine.reset_called_for_testing
        os.remove("config.json")

    def test_sends_reboot_message_to_client(self):
        socket = FakeClientSocket()
        self.configServer.handle_client_request(self.request, socket)
        assert socket.web_page == "rebooting to connect to foo"
        os.remove("config.json")


class FakeClientSocket:

    def send(self, web_page):
        self.web_page = web_page

    def close(self):
        pass
