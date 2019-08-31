import http_support

class TestUnquote:

    def test_handles_empty_string(self):
        assert http_support.unquote("").decode("utf-8") == ""

    def test_handles_normal_string(self):
        assert http_support.unquote("foo bar").decode("utf-8") == "foo bar"

    def test_handles_spaces(self):
        assert http_support.unquote("foo+bar+baz").decode("utf-8") == "foo bar baz"

    def test_handles_url_encoding(self):
        assert http_support.unquote("%23123").decode("utf-8") == "#123"
