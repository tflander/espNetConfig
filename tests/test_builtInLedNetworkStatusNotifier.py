import esp32_machine_emulator.machine as machine
import networkStatusNotifier

## TEMP FOR NOW -- monkeypatch timer
class TimerForMonkeyPatching:

    PERIODIC = 0

    def __init__(self, timerNumber):
        self.timerNumberForTesting = timerNumber
        self.isRunningForTesting = False

    def deinit(self):
        self.isRunningForTesting = False

    def init(self, period, mode=PERIODIC, callback=None):
        self.isRunningForTesting = True

machine.Timer = TimerForMonkeyPatching
### end monkeypatching

def test_init():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    assert notifier.led.pinForTesting == 2
    assert notifier.ledTimer.timerNumberForTesting == 0
    assert notifier.ledTimer.isRunningForTesting

def test_defaultStatusIsDisconnected():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    assert notifier.status == networkStatusNotifier.ConnectStatus.DISCONNECTED
    assert notifier.ledTimer.isRunningForTesting

def test_canSetStatusAsConnected():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setConnected()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTED
    assert notifier.led.value() == 0
    assert not notifier.ledTimer.isRunningForTesting

def test_canSetStatusAsConnecting():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setConnecting()
    assert notifier.status == networkStatusNotifier.ConnectStatus.CONNECTING
    assert notifier.led.value() == 1
    assert not notifier.ledTimer.isRunningForTesting

def test_canSetStatusAsFailed():
    notifier = networkStatusNotifier.BuiltInLedNetworkStatusNotifier()
    notifier.setFailed()
    assert notifier.status == networkStatusNotifier.ConnectStatus.FAILED
    assert notifier.ledTimer.isRunningForTesting

