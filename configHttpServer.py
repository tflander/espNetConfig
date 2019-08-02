import simpleHttpServer, json
try:
    import machine
except:
    import esp32_machine_emulator.machine as machine

import time
_hextobyte_cache = None

def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hextobyte_cache

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
    if _hextobyte_cache is None:
        _hextobyte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hextobyte_cache.get(code)
            if char is None:
                char = _hextobyte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)

class ConfigHttpServer(simpleHttpServer.SimpleHttpServer):

    def __init__(self, serverSocket):
        super(ConfigHttpServer, self).__init__(self.configWebPage, self.requestCallBack, serverSocket)

    def requestCallBack(self, request, clientSocket):
        if len(request) == 0:
            return

        print("request = ", request)
        url = request[0].split(' ')[1]
        if(url.count('ssid=')):
            params = url.split('&')
            ssid = params[0].split('=')[1]
            password = params[1].split('=')[1]
            config = {"ssid": unquote(ssid), "password": unquote(password)}
            print(json.dumps(config))
            f = open("config.json", 'w')
            f.write(json.dumps(config))
            f.close()
            clientSocket.send("rebooting to connect to ")
            clientSocket.send(unquote(ssid))
            clientSocket.close()
            time.sleep(2)
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
