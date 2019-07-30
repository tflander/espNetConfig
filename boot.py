import machine, network, time, socket, json, gc
import networkStatusNotifier

def wifiConnect(ssid, password, netNotifier):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    netNotifier.setConnecting()
    if not waitForNetwork(sta_if, retriesForTimeout=40):
        netNotifier.setFailed()
        print("giving up on network " + ssid)
        # sta_if.disconnect()
        sta_if.active(False) ## prevents background connection errors, but can't create AP: RuntimeError: Wifi Unknown Error 0x0005
        return None, None
    netNotifier.setConnected()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    return addr, sta_if.ifconfig()

def waitForNetwork(sta_if, retriesForTimeout):
    count = 0
    while not sta_if.isconnected():
        time.sleep_ms(200)
        count += 1
        if(count > retriesForTimeout):
            return False
    return True

def startApConfigServer():
    gc.collect()
    print('connect to http://192.168.4.1 to configure')
    configServer = netConfig.NetConfig("tfDemo")
    configServer.start()

import config, netConfig
def foo():
    netNotifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()

    existingConfig = config.Config.read('config.json')
    if existingConfig.exists:
        print('connecting to ' + existingConfig.ssid + '...')
        addr, ifConfig = wifiConnect(existingConfig.ssid, existingConfig.password, netNotifier)
        print(addr)
        if not addr:
            print('connect failed')
            startApConfigServer()
    else:
        startApConfigServer()
