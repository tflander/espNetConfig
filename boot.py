import machine, network, time, socket, json
import networkStatusNotifier

def wifiConnect(ssid, password):
    onboardLed = machine.Pin(2, machine.Pin.OUT)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    onboardLed.on()
    waitForNetwork(sta_if)
    onboardLed.off()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    return addr, sta_if.ifconfig()

def waitForNetwork(sta_if):
    while not sta_if.isconnected():
        time.sleep_ms(200)

netNotifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()

import netConfig
def foo():
    c = netConfig.NetConfig("tfDemo")
    c.start()
