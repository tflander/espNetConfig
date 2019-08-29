import http_request


class SimpleHttpServer:

    def __init__(self, webResponseCallback, requestHandlerCallback, serverSocket):
        self.webResponseCallback = webResponseCallback
        self.serverSocket = serverSocket
        self.requestHandlerCallback = requestHandlerCallback

    # TODO: wrap server socket in response object?
    def respondtoClient(self):
        clientSocket, addr = self.serverSocket.accept()
        # request = self.readRequestHeader(clientSocket)
        req = http_request.HttpRequest(clientSocket)
        self.requestHandlerCallback(req)
        clientSocket.send(self.webResponseCallback())
        clientSocket.close()
