from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

class RestController:

    __encoding__ = 'UTF-8'

    def __init__(self, base_url = '', port = 8000) -> None:
        self.base_url = base_url
        self.port = port

    def get(self, httpHandler: BaseHTTPRequestHandler):
        pass

    def add_header(self, httpHandler: BaseHTTPRequestHandler, keyword: str, value: str):
        httpHandler.send_header(keyword, value)
        httpHandler.end_headers()

    def write(self, httpHandler: BaseHTTPRequestHandler, value: Any):
        httpHandler.wfile.write(value.encode(self.__encoding__))

    def __create_handler(rest_self):
        class MyHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                rest_self.get(self)
        return MyHandler

    def run(self, server_class=HTTPServer):
        server_address = (self.base_url, self.port)
        handler_class = self.__create_handler()
        httpd = server_class(server_address, handler_class)
        httpd.rest_controller = self
        httpd.serve_forever()


class Test(RestController):

    def get(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        self.add_header(httpHandler, 'Content-type', 'text/html')
        self.write(httpHandler, 'Hello, world!')


test = Test()
test.run()

