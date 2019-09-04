import gc
import socket
import time

import network

import config
import httpLocalHostListener
import netConfigAccessPoint
import networkStatusNotifier


def connect_network_or_go_into_config_mode(ssid_for_ap_connection, network_config_notifier=None):
    net_notifier = get_net_notifier(network_config_notifier)
    existing_config = config.Config.read('config.json')
    if existing_config.exists:
        print('connecting to ' + existing_config.ssid + '...')
        local_address, if_config = wifi_connect(existing_config.ssid, existing_config.password, net_notifier)
        print(local_address)
        if not local_address:
            print('connect failed')
            net_notifier.setFailed()
            start_ap_config_server(ssid_for_ap_connection, number_of_listeners=5)
    else:
        net_notifier.setDisconnected()
        start_ap_config_server(ssid_for_ap_connection, number_of_listeners=5)


def get_net_notifier(network_config_notifier):
    net_notifier = network_config_notifier
    if not net_notifier:
        net_notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    return net_notifier


def wifi_connect(remote_sid, password, net_notifier):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(remote_sid, password)
    net_notifier.setConnecting()
    if not wait_for_network(sta_if, retries_for_timeout=80):
        net_notifier.setFailed()
        print("giving up on network " + remote_sid)
        sta_if.active(False)
        return None, None
    net_notifier.setConnected()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    return addr, sta_if.ifconfig()


def wait_for_network(sta_if, retries_for_timeout):
    count = 0
    while not sta_if.isconnected():
        time.sleep_ms(200)
        count += 1
        if count > retries_for_timeout:
            return False
    return True


def start_ap_config_server(new_ap_ssid, number_of_listeners):
    gc.collect()
    print('connect to http://192.168.4.1 to configure')
    http_local_host_listener = create_http_local_host_listener(number_of_listeners)
    config_server = netConfigAccessPoint.NetConfigAccessPoint(new_ap_ssid, http_local_host_listener)
    config_server.start()


def create_http_local_host_listener(number_of_listeners):
    return httpLocalHostListener.HttpLocalHostListener(number_of_listeners)
