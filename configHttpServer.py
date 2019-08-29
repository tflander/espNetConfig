import simpleHttpServer, json
import machine
import time
_hex_byte_cache = None


def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hex_byte_cache

    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        return b''

    if isinstance(string, str):
        string = string.replace('+', ' ')
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    # Build cache for hex to char mapping on-the-fly only for codes
    # that are actually used
    if _hex_byte_cache is None:
        _hex_byte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hex_byte_cache.get(code)
            if char is None:
                char = _hex_byte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)


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

    def __init__(self, server_socket, config_web_page=None):
        if not config_web_page:
            config_web_page = default_config_web_page
        super(ConfigHttpServer, self).__init__(config_web_page, self.handle_client_request, server_socket)

    def handle_client_request(self, req):

        if req.params.get('ssid'):
            station_id = req.params.get('ssid')
            password = req.params.get('password')
            config = {"ssid": unquote(station_id).decode("utf-8"), "password": unquote(password).decode("utf-8")}
            # print(json.dumps(config))
            self.write_config(config)
            self.reboot_device(req, station_id)

    def reboot_device(self, req, station_id):
        client_socket = req.client_socket
        client_socket.send(self.rebooting_web_page(station_id))
        client_socket.close()
        time.sleep(2)
        machine.reset()

    @staticmethod
    def write_config(config):
        f = open("config.json", 'w')
        f.write(json.dumps(config))
        f.close()

    @staticmethod
    def rebooting_web_page(station_id):
        return "rebooting to connect to " + unquote(station_id).decode("utf-8")
