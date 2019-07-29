from enum import Enum

class ConnectStatus(Enum):
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

class BuiltInLedNetworkStatusNotifier(NetworkStatusNotifier):
    pass