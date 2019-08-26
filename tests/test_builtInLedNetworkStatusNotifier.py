import networkStatusNotifier


def test_init():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    assert notifier.led.pinForTesting == 2
    assert notifier.ledTimer.timer_id_for_testing == 0
    assert notifier.ledTimer.is_running_for_testing


def test_default_status_is_disconnected():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    assert notifier.status == networkStatusNotifier.ConnectStatus.DISCONNECTED
    assert notifier.ledTimer.is_running_for_testing


def test_set_status_as_connected():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setConnected()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTED
    assert notifier.led.value() == 0
    assert not notifier.ledTimer.is_running_for_testing


def test_set_status_as_connecting():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setConnecting()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTING
    assert notifier.led.value() == 1
    assert not notifier.ledTimer.is_running_for_testing


def test_set_status_as_failed():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setFailed()
    assert notifier.status == networkStatusNotifier.ConnectStatus.FAILED
    assert notifier.ledTimer.is_running_for_testing

