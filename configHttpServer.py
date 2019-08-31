import time

import machine

import json
import simpleHttpServer


class ConfigHttpServer(simpleHttpServer.SimpleHttpServer):

    def __init__(self, max_concurrent_requests):
        super(ConfigHttpServer, self).__init__(self.route_client_request, max_concurrent_requests)
        self.form_submission_controller = FormSubmissionController()
        self.form_display_controller = FormDisplayController()

    def route_client_request(self, req, resp):

        if req.params.get('ssid'):
            self.form_submission_controller.handle_form_submission(req, resp)
        else:
            self.form_display_controller.display_form(resp)


class FormDisplayController:

    def display_form(self, resp):
        resp.send(self.default_config_web_page())

    @staticmethod
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


class FormSubmissionController:
    def handle_form_submission(self, req, resp):
        station_id = req.params.get('ssid')
        password = req.params.get('password')
        config = {"ssid": station_id, "password": password}
        self.write_config(config)
        resp.send(self.rebooting_web_page(station_id))
        self.reboot_device()

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
