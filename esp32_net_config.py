import network, time, socket, gc
import networkStatusNotifier
import config, netConfigAccessPoint
import httpLocalHostListener


def connect_network_or_go_into_config_mode(ssid_for_ap_connection, network_config_notifier=None):

    existing_config = config.Config.read('config.json')
    if existing_config.exists:
        print('connecting to ' + existing_config.ssid + '...')
        addr, ifConfig = wifiConnect(existing_config.ssid, existing_config.password, network_config_notifier)
        print(addr)
        if not addr:
            print('connect failed')
            startApConfigServer(ssid_for_ap_connection)
    else:
        startApConfigServer(ssid_for_ap_connection)


def wifiConnect(ssid, password, network_config_notifier=None):

    net_notifier = network_config_notifier
    if not net_notifier:
        net_notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    net_notifier.setConnecting()
    if not waitForNetwork(sta_if, retriesForTimeout=80):
        net_notifier.setFailed()
        print("giving up on network " + ssid)
        sta_if.active(False)
        return None, None
    net_notifier.setConnected()

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


def startApConfigServer(ssid):
    gc.collect()
    print('connect to http://192.168.4.1 to configure')
    http_local_host_listener = create_http_local_host_listener(numberOfListeners=5)
    configServer = netConfigAccessPoint.NetConfigAccessPoint(ssid, http_local_host_listener)
    configServer.start()


def create_http_local_host_listener(numberOfListeners):
    return httpLocalHostListener.HttpLocalHostListener(numberOfListeners)