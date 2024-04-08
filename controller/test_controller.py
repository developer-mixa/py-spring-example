from utils.rest_controller import RestController
from http.server import BaseHTTPRequestHandler

class Test(RestController):

    def init_routes(self):
        self.add_get_route('/hello', self.get_hello)
        self.add_get_route('/hello2', self.get_hello_2)
        self.add_get_route('/', self.index_test)

    def get_hello(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        self.write(httpHandler, 'Hello, world!')

    def get_hello_2(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        self.write(httpHandler, 'Hello, world2!')

    def index_test(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        self.write(httpHandler, 'Index html')
\
if __name__ == '__main__':
    test = Test()
    test.run()