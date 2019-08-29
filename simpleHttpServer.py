import http


class SimpleHttpServer:

    def __init__(self, client_request_router, serverSocket):
        self.serverSocket = serverSocket
        self.client_request_router = client_request_router

    def respondtoClient(self):
        clientSocket, addr = self.serverSocket.accept()
        req = http.HttpRequest(clientSocket)
        resp = http.HttpResponse(clientSocket)
        self.client_request_router(req, resp)
