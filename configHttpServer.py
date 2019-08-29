import simpleHttpServer, json
import machine
import time


def default_config_web_page():
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


class ConfigHttpServer(simpleHttpServer.SimpleHttpServer):

    def __init__(self, server_socket):
        super(ConfigHttpServer, self).__init__(self.handle_client_request, server_socket)

    def handle_client_request(self, req, resp):

        if req.params.get('ssid'):
            station_id = req.params.get('ssid')
            password = req.params.get('password')
            config = {"ssid": station_id, "password": password}
            self.write_config(config)
            resp.send(self.rebooting_web_page(station_id))
            self.reboot_device()
        else:
            resp.send(default_config_web_page())

    @staticmethod
    def reboot_device():
        time.sleep(2)
        machine.reset()

    @staticmethod
    def write_config(config):
        f = open("config.json", 'w')
        f.write(json.dumps(config))
        f.close()

    @staticmethod
    def rebooting_web_page(station_id):
        return "rebooting to connect to " + station_id
