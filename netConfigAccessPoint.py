import network
import socket
import configHttpServer


class NetConfigAccessPoint:

    def __init__(self, localSsid, httpLocalHostListener):
        self.ssid = localSsid
        self.serverSocket = httpLocalHostListener.listener_socket

    def start(self):

        self.create_access_point()  # address is always http://192.168.4.1
        http_server = configHttpServer.ConfigHttpServer(self.serverSocket)

        while True:
            http_server.respondtoClient()

    def create_access_point(self):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        ap_if.config(essid=self.ssid) # fails if we tried to go to st mode..
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        return addr, ap_if.ifconfig()
