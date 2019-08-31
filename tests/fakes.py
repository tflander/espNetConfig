import simpleHttpServer

class FakeClientSocket:

    def __init__(self):
        self.request = None
        self.web_page = None

    def send(self, web_page):
        self.web_page = web_page

    def close(self):
        pass

    # noinspection PyUnusedLocal
    def makefile(self, unused1, unused2):
        return FakeRequestHeaderSocket(self.request)

    def expect_request(self, request):
        self.request = request


class FakeRequestHeaderSocket:

    def __init__(self, request):
        self.request = request
        self.index = 0

    def readline(self):
        if self.index == len(self.request):
            return b'\r\n'
        request_line = self.request[self.index]
        self.index += 1
        return request_line.encode('utf-8')


class FakeHttpServer(simpleHttpServer.SimpleHttpServer):

    def __init__(self, real_http_server):
        super(FakeHttpServer, self).__init__(real_http_server.client_request_router, real_http_server.max_concurrent_requests)
        self.create_listener = lambda  : FakeLocalHostListener()
        self.init()

    def expect_request(self, request):
        self.listener.listener_socket.client_socket.expect_request(request)


class FakeLocalHostListener:

    def __init__(self):
        self.listener_socket = FakeListenerSocket(FakeClientSocket())


class FakeListenerSocket:

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.listener_socket = "stub"

    def accept(self):
        return self.client_socket, "client address"
