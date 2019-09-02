import http_support
import httpLocalHostListener


class SimpleHttpServer:

    def __init__(self, client_request_router, max_concurrent_requests):
        self.max_concurrent_requests = max_concurrent_requests
        self.client_request_router = client_request_router
        self.listener = None

    def init(self):
        self.listener = self.create_listener()

    def dispatch_client_requests(self):
        client_socket, addr = self.listener.listener_socket.accept()
        req = http_support.HttpRequest(client_socket)
        resp = http_support.HttpResponse(client_socket)
        self.client_request_router(req, resp)

    def create_listener(self):
        return httpLocalHostListener.HttpLocalHostListener(self.max_concurrent_requests)
