import http_support
import tests.fakes


def test_response():
    client_socket = tests.fakes.FakeClientSocket()
    resp = http_support.HttpResponse(client_socket)
    resp.send("foo")

    assert client_socket.web_page == "foo"
