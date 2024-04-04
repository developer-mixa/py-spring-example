from http.server import HTTPServer, BaseHTTPRequestHandler

class RestController:

    def __init__(self, base_url = '', port = 8000) -> None:
        self.base_url = base_url
        self.port = port

    def get(self, httpHandler: BaseHTTPRequestHandler):
        pass

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
        httpHandler.send_header('Content-type', 'text/html')
        httpHandler.end_headers()
        content = 'Hello, world!'
        httpHandler.wfile.write(content.encode('UTF-8'))

    def __init__(self, base_url='', port=8000) -> None:
        super().__init__(base_url, port)

test = Test()
test.run()

