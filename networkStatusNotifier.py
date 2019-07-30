try:
    import machine
except:
    import esp32_machine_emulator.machine as machine


class ConnectStatus():
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    FAILED = 3

class NetworkStatusNotifier:

    def __init__(self):
        self.status = ConnectStatus.DISCONNECTED

    def setConnected(self):
        self.status = ConnectStatus.CONNECTED

    def setConnecting(self):
        self.status = ConnectStatus.CONNECTING

    def setFailed(self):
        self.status = ConnectStatus.FAILED

    def setDisconnected(self):
        self.status = ConnectStatus.DISCONNECTED


class BuiltInLedNetworkStatusNotifier(NetworkStatusNotifier):

    def __init__(self):
        super(BuiltInLedNetworkStatusNotifier, self).__init__()
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.led.off()
        self.ledTimer = machine.Timer(0)
        self.setDisconnected()

    def setConnecting(self):
        super(BuiltInLedNetworkStatusNotifier, self).setConnecting()
        self.ledTimer.deinit()
        self.led.on()

    def setConnected(self):
        super(BuiltInLedNetworkStatusNotifier, self).setConnected()
        self.ledTimer.deinit()
        self.led.off()

    def setFailed(self):
        super(BuiltInLedNetworkStatusNotifier, self).setFailed()
        self.ledTimer.init(period=100, callback=self.toggleLedCallback)

    def setDisconnected(self):
        super(BuiltInLedNetworkStatusNotifier, self).setDisconnected()
        self.ledTimer.init(period=500, callback=self.toggleLedCallback)

    def toggleLedCallback(self, timer):
        if(self.led.value()):
            self.led.off()
        else:
            self.led.on()

