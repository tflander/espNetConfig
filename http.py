class HttpRequest():

    def __init__(self, client_socket):
        self.client_socket = client_socket
        cl_file = client_socket.makefile('rwb', 0)  # TODO: does the buffer really need to be writable?
        self.raw_request_headers = self.get_raw_request_headers(cl_file)
        self.params = {}
        self.path = ''
        self.parse_path()

    @staticmethod
    def get_raw_request_headers(cl_file):
        request_headers = []
        while True:
            line = cl_file.readline()
            request_headers.append(line.decode('utf-8'))
            if not line or line == b'\r\n':
                break
        return request_headers

    def parse_path(self):
        url = self.raw_request_headers[0].split(' ')[1]
        path_and_raw_params = url.split('?')
        self.path = path_and_raw_params[0]

        if len(path_and_raw_params) == 1:
            return
        param_pairs = path_and_raw_params[1].split('&')

        for param_pair in param_pairs:
            split = param_pair.split('=')
            self.params.__setitem__(split[0], split[1])


class HttpResponse():

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def send(self, content):
        self.client_socket.send(content)
        self.client_socket.close()
