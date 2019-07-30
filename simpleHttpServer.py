import json

class SimpleHttpServer:

    def __init__(self, fGetWebResponseHtml, serverSocket):
        self.fGetWebResponseHtml = fGetWebResponseHtml
        self.serverSocket = serverSocket

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
        url = request[0].split(' ')[1]
        if(url.count('ssid=')):
            params = url.split('&')
            ssid = params[0].split('=')[1]
            password = params[1].split('=')[1]
            config = {"ssid": ssid, "password": password}
            print(json.dumps(config))
            f = open("config.json", 'w')
            f.write(json.dumps(config))
            f.close()
        clientSocket.send(self.fGetWebResponseHtml())
        clientSocket.close()
