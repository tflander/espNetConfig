import machine, time

greenLed = machine.Pin(22, machine.Pin.OUT)
redLed = machine.Pin(21, machine.Pin.OUT)

while True:
    greenLed.on()
    redLed.off()
    time.sleep(1)
    greenLed.off()
    redLed.on()
    time.sleep(1)