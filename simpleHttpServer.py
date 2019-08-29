import http


class SimpleHttpServer:

    def __init__(self, webResponseCallback, requestHandlerCallback, serverSocket):
        self.webResponseCallback = webResponseCallback
        self.serverSocket = serverSocket
        self.requestHandlerCallback = requestHandlerCallback

    # TODO: wrap server socket in response object?
    def respondtoClient(self):
        clientSocket, addr = self.serverSocket.accept()
        req = http.HttpRequest(clientSocket)
        self.requestHandlerCallback(req)
        clientSocket.send(self.webResponseCallback()) # TODO: don't want to display default page if we've responded
        clientSocket.close()
