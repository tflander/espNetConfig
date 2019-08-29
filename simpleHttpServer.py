import http


class SimpleHttpServer:

    def __init__(self, requestHandlerCallback, serverSocket):
        self.serverSocket = serverSocket
        self.requestHandlerCallback = requestHandlerCallback

    def respondtoClient(self):
        clientSocket, addr = self.serverSocket.accept()
        req = http.HttpRequest(clientSocket)
        resp = http.HttpResponse(clientSocket)
        self.requestHandlerCallback(req, resp)
