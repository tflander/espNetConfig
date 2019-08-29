class FakeClientSocket():

    def __init__(self, request):
        self.request = request
        self.web_page = None

    def send(self, web_page):
        self.web_page = web_page

    def close(self):
        pass

    def makefile(self, unused1, unused2):
        return FakeRequestSocket(self.request)


class FakeRequestSocket:

    def __init__(self, request):
        self.request = request
        self.index = 0

    def readline(self):
        if self.index == len(self.request):
            return b'\r\n'
        request_line = self.request[self.index]
        self.index += 1
        return request_line.encode('utf-8')
