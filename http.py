_hex_byte_cache = None


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
            self.params.__setitem__(unquote(split[0]).decode('utf-8'), unquote(split[1]).decode('utf-8'))


class HttpResponse():

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def send(self, content):
        self.client_socket.send(content)
        self.client_socket.close()


def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hex_byte_cache

    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        return b''

    if isinstance(string, str):
        string = string.replace('+', ' ')
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    # Build cache for hex to char mapping on-the-fly only for codes
    # that are actually used
    if _hex_byte_cache is None:
        _hex_byte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hex_byte_cache.get(code)
            if char is None:
                char = _hex_byte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)

