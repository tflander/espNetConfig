import os.path

import machine

import configHttpServer
import tests.fakes


class TestRespondToClient:
    form_submitted_request = ['GET /?ssid=foo+bar&password=bar HTTP/1.1\r\n']
    form_display_request = ['GET / HTTP/1.1\r\n']

    def test_writes_config_file(self):
        config_server = self.create_config_server(self.form_submitted_request)
        config_server.dispatch_client_requests()

        assert os.path.exists("config.json")
        f = open("config.json")
        assert f.read() == '{"ssid": "foo bar", "password": "bar"}'
        os.remove("config.json")

    def test_exits_if_empty_request(self):
        empty_request = ['GET ']
        config_server = self.create_config_server(empty_request)
        config_server.dispatch_client_requests()
        assert not os.path.exists("config.json")

    def test_reboots_device(self):
        config_server = self.create_config_server(self.form_submitted_request)
        config_server.dispatch_client_requests()
        assert machine.reset_called_for_testing
        os.remove("config.json")

    def test_sends_config_form_to_client(self):
        config_server = self.create_config_server(self.form_display_request)
        config_server.dispatch_client_requests()
        socket = config_server.listener.listener_socket.client_socket
        assert socket.web_page.__contains__("<h2>Configure Network</h2>")

    def test_sends_reboot_message_to_client(self):
        config_server = self.create_config_server(self.form_submitted_request)
        config_server.dispatch_client_requests()
        socket = config_server.listener.listener_socket.client_socket
        assert socket.web_page == "rebooting to connect to foo bar"
        os.remove("config.json")

    @staticmethod
    def create_config_server(request):
        config_server = configHttpServer.ConfigHttpServer(max_concurrent_requests=5)
        server = tests.fakes.FakeHttpServer(config_server)
        server.expect_request(request)
        return server

