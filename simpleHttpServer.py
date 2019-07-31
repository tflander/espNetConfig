import json

class SimpleHttpServer:

    def __init__(self, webResponseCallback, requestHandlerCallback, serverSocket):
        self.webResponseCallback = webResponseCallback
        self.serverSocket = serverSocket
        self.requestHandlerCallback = requestHandlerCallback

    def readRequestHeader(self, clientSocket):
        cl_file = clientSocket.makefile('rwb', 0)  # TODO: does the buffer really need to be writable?
        request = []
        while True:
            line = cl_file.readline()
            request.append(line.decode('utf-8'))
            if not line or line == b'\r\n':
                break

        return request

    def respondtoClient(self):
        clientSocket, addr = self.serverSocket.accept()
        request = self.readRequestHeader(clientSocket)
        self.requestHandlerCallback(request, clientSocket)
        clientSocket.send(self.webResponseCallback())
        clientSocket.close()
