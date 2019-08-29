import http
import tests.fakes


def test_path_parsed():
    req = create_request(['GET /?ssid=foo&password=bar HTTP/1.1\r\n'])
    assert req.path == '/'


def test_path_for_empty_request():
    req = create_request(['GET '])
    assert req.path == ''


def test_parameters_parsed():
    req = create_request(['GET /?ssid=foo&password=bar HTTP/1.1\r\n'])
    assert req.params == {'ssid': 'foo', 'password': 'bar'}


def create_request(request):
    client_socket = tests.fakes.FakeClientSocket(request)
    req = http.HttpRequest(client_socket)
    return req
