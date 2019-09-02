import http


class SimpleHttpServer:

    def __init__(self, client_request_router, listener_socket):
        self.listener_socket = listener_socket
        self.client_request_router = client_request_router

    def dispatch_client_requests(self):
        client_socket, addr = self.listener_socket.accept()
        req = http.HttpRequest(client_socket)
        resp = http.HttpResponse(client_socket)
        self.client_request_router(req, resp)
