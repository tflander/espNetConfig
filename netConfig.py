import network, socket
import configHttpServer


class NetConfig:

    def __init__(self, localSsid):
        self.ssid = localSsid
        self.serverSocket = self.bindHttpLocalHost(numberOfListeners=5)

    def start(self):

        self.createAccessPoint()  # address is always http://192.168.4.1
        httpServer = configHttpServer.ConfigHttpServer(self.serverSocket)

        while True:
            httpServer.respondtoClient()

    def createAccessPoint(self):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        ap_if.config(essid=self.ssid) # fails if we tried to go to st mode..
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        return addr, ap_if.ifconfig()

    def bindHttpLocalHost(self, numberOfListeners):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80)) # TODO: retry logic?...OSError:112
        s.listen(numberOfListeners)
        return s
