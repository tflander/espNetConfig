import simpleHttpServer

class ConfigHttpServer(simpleHttpServer.SimpleHttpServer):

    def __init__(self, serverSocket):
        super(ConfigHttpServer, self).__init__(self.configWebPage, serverSocket)

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
