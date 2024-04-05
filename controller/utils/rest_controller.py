from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

class RestController:

    # Constants
    __ENCODING = 'UTF-8'
    __auto_add_header__ = True
    __CONTENT_TYPE = 'Content-type'
    __TEXT_HTML = 'text/html'

    #All queries with routes
    _get_queries = {}
    _post_queries = {}
    _put_queries = {}
    _delete_queries = {}
    
    #Base init
    def __init__(self, base_url = '', port = 8000) -> None:
        self.base_url = base_url
        self.port = port
        self.init_routes()

    def init_routes(self):
        pass

    #Add-route methods
    def add_get_route(self, query, function):
        self._get_queries[query] = function
    
    def add_post_route(self, query, function):
        self._post_queries[query] = function

    def add_put_route(self, query, function):
        self._put_queries[query] = function

    def add_delete_route(self, query, function):
        self._delete_queries[query] = function

    #helper methods
    def add_header(self, httpHandler: BaseHTTPRequestHandler, keyword: str, value: str):
        httpHandler.send_header(keyword, value)
        httpHandler.end_headers()

    def add_default_header(self, httpHandler: BaseHTTPRequestHandler):
        self.add_header(httpHandler, self.__CONTENT_TYPE, self.__TEXT_HTML)

    def write(self, httpHandler: BaseHTTPRequestHandler, value: Any):
        httpHandler.wfile.write(value.encode(self.__ENCODING))

    #Create handler with our routes
    def __create_handler(self):
        def handler_factory(rest_controller):
            class MyHandler(BaseHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    self.rest_controller = rest_controller
                    super().__init__(*args, **kwargs)

                def do_GET(self):
                    if self.path == '/favicon.ico':
                        return
                    for query, get_func in self.rest_controller._get_queries.items():                        
                        if(self.path == query):
                            get_func(self)
                            break

                def do_POST(self):
                    if self.path == '/favicon.ico':
                        return
                    for query, post_func in self.rest_controller._post_queries.items():                        
                        if(self.path == query):
                            post_func(self)
                            break

                def do_PUT(self):
                    if self.path == '/favicon.ico':
                        return
                    for query, put_func in self.rest_controller._put_queries.items():                        
                        if(self.path == query):
                            put_func(self)
                            break

                def do_DELETE(self):
                    if self.path == '/favicon.ico':
                        return
                    for query, delete_func in self.rest_controller._delete_queries.items():                        
                        if(self.path == query):
                            delete_func(self)
                            break

            return MyHandler

        return handler_factory(self)
    
    #Run our server
    def run(self, server_class=HTTPServer):
        server_address = (self.base_url, self.port)
        handler_class = self.__create_handler()
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()