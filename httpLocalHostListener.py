import socket
import gc
import time
import network


class HttpLocalHostListener:

    def __init__(self, numberOfListeners):
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(False)
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        gc.collect()
        time.sleep(2)
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.listener_socket.bind(('', 80))  # TODO: retry logic?...OSError:112
        self.listener_socket.listen(numberOfListeners)
