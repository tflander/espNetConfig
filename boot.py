import machine, network, time, socket, json, gc
import networkStatusNotifier

def wifiConnect(ssid, password):
    onboardLed = machine.Pin(2, machine.Pin.OUT)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    onboardLed.on()
    if not waitForNetwork(sta_if, maxRetries=20):
        print("giving up on network " + ssid)
        sta_if.disconnect()
        sta_if.active(False) ## prevents background connection errors, but can't create AP: RuntimeError: Wifi Unknown Error 0x0005
        return None, None
    onboardLed.off()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    return addr, sta_if.ifconfig()

def waitForNetwork(sta_if, maxRetries):
    count = 0
    while not sta_if.isconnected():
        time.sleep_ms(200)
        count += 1
        if(count > maxRetries):
            return False
    return True

netNotifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
def startApConfigServer():
    gc.collect()
    print('connect to http://192.168.4.1 to configure')
    configServer = netConfig.NetConfig("tfDemo")
    configServer.start()


def grumble():
    gc.collect()
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("badSsid", "badPassword")

    # assume we waited for failure and decided to launch in AP mode to serve page for connection configuration

    sta_if.disconnect()
    sta_if.active(False)

    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid="doomedSsid")  # RuntimeError: Wifi Unknown Error 0x0005


import config, netConfig
def foo():
    existingConfig = config.Config.read('config.json')
    if existingConfig.valid:
        print('connecting to ' + existingConfig.ssid + '...')
        addr, ifConfig = wifiConnect(existingConfig.ssid, existingConfig.password)
        print(addr)
        if not addr:
            print('connect failed')
            startApConfigServer()
    else:
        startApConfigServer()
