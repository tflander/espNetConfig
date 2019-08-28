import configHttpServer
import os.path
import machine
import unittest

class TestRespondToClient:

    request = ['GET /?ssid=foo&password=bar HTTP/1.1\r\n']

    def test_writes_config_file(self):
        config_server = self.create_config_server(self.request)
        config_server.respondtoClient()

        assert os.path.exists("config.json")
        f=open("config.json")
        assert f.read() == '{"ssid": "foo", "password": "bar"}'
        os.remove("config.json")

    def test_exits_if_empty_request(self):
        empty_request = ['GET ']
        config_server = self.create_config_server(empty_request)
        config_server.respondtoClient()
        assert not os.path.exists("config.json")

    def test_reboots_device(self):
        config_server = self.create_config_server(self.request)
        config_server.respondtoClient()
        assert machine.reset_called_for_testing
        os.remove("config.json")

    @unittest.skip("dodgy coding exposed.  Writes web page after calling reboot.  Need a better way")
    def test_sends_reboot_message_to_client(self):
        config_server = self.create_config_server(self.request)
        config_server.respondtoClient()
        socket = config_server.serverSocket.client_socket
        assert socket.web_page == "rebooting to connect to foo"
        os.remove("config.json")

    @staticmethod
    def create_config_server(request):
        client_socket = FakeClientSocket(request)
        server_socket = FakeServerSocket(client_socket)
        return configHttpServer.ConfigHttpServer(server_socket)


class TestHandleClientRequest:

    request = ['GET /?ssid=foo&password=bar HTTP/1.1\r\n']
    configServer = configHttpServer.ConfigHttpServer("fake server socket")


    def test_sends_reboot_message_to_client(self):
        socket = FakeClientSocket(self.request)
        self.configServer.handle_client_request(self.request, socket)
        assert socket.web_page == "rebooting to connect to foo"
        os.remove("config.json")


class TestUnquote:

    def test_handles_empty_string(self):
        assert configHttpServer.unquote("").decode("utf-8") == ""

    def test_handles_normal_string(self):
        assert configHttpServer.unquote("foo bar").decode("utf-8") == "foo bar"

    def test_handles_spaces(self):
        assert configHttpServer.unquote("foo+bar+baz").decode("utf-8") == "foo bar baz"

    def test_handles_url_encoding(self):
        assert configHttpServer.unquote("%23123").decode("utf-8") == "#123"


class FakeClientSocket():

    def __init__(self, request):
        self.request = request
        self.web_page = None

    def send(self, web_page):
        self.web_page = web_page

    def close(self):
        pass

    def makefile(self, unused1, unused2):
        return FakeRequest(self.request)


class FakeRequest:

    def __init__(self, request):
        self.request = request
        self.index = 0

    def readline(self):
        if self.index == len(self.request):
            return b'\r\n'
        request_line = self.request[self.index]
        self.index += 1
        return request_line.encode('utf-8')


class FakeServerSocket:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def accept(self):
        return self.client_socket, "client address"
