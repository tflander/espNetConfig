import networkStatusNotifier

def test_init():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    assert notifier.led.pinForTesting == 2

def test_defaultStatusIsDisconnected():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    assert notifier.status == networkStatusNotifier.ConnectStatus.DISCONNECTED
    assert notifier.led.value() == 0 # TODO: needs to be flashing

def test_canSetStatusAsConnected():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setConnected()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTED
    assert notifier.led.value() == 0

def test_canSetStatusAsConnecting():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setConnecting()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTING
    assert notifier.led.value() == 1

def test_canSetStatusAsFailed():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setFailed()
    assert notifier.status == networkStatusNotifier.ConnectStatus.FAILED
    assert notifier.led.value() == 0 # TODO: needs to be flashing

