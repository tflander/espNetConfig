import simpleHttpServer, json
try:
    import machine
except:
    import esp32_machine_emulator.machine as machine

class ConfigHttpServer(simpleHttpServer.SimpleHttpServer):

    def __init__(self, serverSocket):
        super(ConfigHttpServer, self).__init__(self.configWebPage, self.requestCallBack, serverSocket)

    def requestCallBack(self, request):
        print(request)
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
            machine.reset()

    def configWebPage(self):
        return """
    <!DOCTYPE html>
    <html>
    <body>

    <h2>Configure Network</h2>
    <p>enter your network ssid and password</p>

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
