import networkStatusNotifier

def test_defaultStatusIsDisconnected():
    notifier = networkStatusNotifier.NetworkStatusNotifier()
    assert notifier.status == networkStatusNotifier.ConnectStatus.DISCONNECTED

def test_canSetStatusAsConnected():
    notifier = networkStatusNotifier.NetworkStatusNotifier()
    notifier.setConnected()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTED

def test_canSetStatusAsConnecting():
    notifier = networkStatusNotifier.NetworkStatusNotifier()
    notifier.setConnecting()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTING

def test_canSetStatusAsFailed():
    notifier = networkStatusNotifier.NetworkStatusNotifier()
    notifier.setFailed()
    assert notifier.status == networkStatusNotifier.ConnectStatus.FAILED

def test_canSetStatusAsDisconnected():
    notifier = networkStatusNotifier.NetworkStatusNotifier()
    notifier.setDisconnected()
    assert notifier.status == networkStatusNotifier.ConnectStatus.DISCONNECTED
