import socket


class HttpLocalHostListener:

    def __init__(self, numberOfListeners):
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.bind(('', 80))  # TODO: retry logic?...OSError:112
        self.listener_socket.listen(numberOfListeners)
