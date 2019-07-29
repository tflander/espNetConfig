import machine, network, time, socket, json

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

def createAccessPoint(ssid):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid=ssid)
    ap_if.active(True)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    return addr, ap_if.ifconfig()

def bindHttpLocalHost(numberOfListeners):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(numberOfListeners)
    return s

def readRequestHeader(clientSocket):
    cl_file = clientSocket.makefile('rwb', 0)  # TODO: does the buffer really need to be writable?
    incomingData = []
    while True:
        line = cl_file.readline()
        incomingData.append(line.decode('utf-8'))
        if not line or line == b'\r\n':
            break

    return incomingData


class OnePageHttpServer:

    def __init__(self, fGetWebResponseHtml, serverSocket):
        self.fGetWebResponseHtml = fGetWebResponseHtml
        self.serverSocket = serverSocket

    def respondtoClient(self):
        clientSocket, addr = self.serverSocket.accept()
        request = readRequestHeader(clientSocket)
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

def configWebPage():
    return """
<!DOCTYPE html>
<html>
<body>

<h2>Configure Network</h2>
<p>The <strong>input type="text"</strong> defines a one-line text input field:</p>

<form action="">
ssid:<br>
<input type="text" name="ssid">
<br>
password:<br>
<input type="text" name="password">
<br><br>
<input type="submit">
</form>

</body>
</html>
    """

def foo():
    addr, config = createAccessPoint("toddGRDemo")
    print(addr)
    print(config)
    serverSocket = bindHttpLocalHost(numberOfListeners=5)
    httpServer = OnePageHttpServer(configWebPage, serverSocket)

    while True:
        httpServer.respondtoClient()
