import http
import tests.fakes


def test_foo():
    client_socket = tests.fakes.FakeClientSocket(None)  # TODO: dodgy to pass None
    resp = http.HttpResponse(client_socket)
    resp.send("foo")
    resp.close()

    assert client_socket.web_page == "foo"