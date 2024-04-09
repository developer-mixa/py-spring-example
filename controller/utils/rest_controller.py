from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

class RestController:

    # Constants
    __ENCODING = 'UTF-8'
    __auto_add_header__ = True
    __CONTENT_TYPE = 'Content-type'
    __TEXT_HTML = 'text/html'

    #Settings
    __IP__ = ''
    __BASE_URL__ = ''
    __PORT__ = 8000

    #All queries with routes
    __get_queries = {}
    __post_queries = {}
    __put_queries = {}
    __delete_queries = {}
    
    #Base init
    def __init__(self) -> None:
        self.init_routes()

    def init_routes(self):
        pass

    #Add-route methods

    def __add_route(self,map, query, function):
        map[self.__BASE_URL__ + query] = function

    def add_get_route(self, query, function):
        self.__add_route(self.__get_queries, query, function)
    
    def add_post_route(self, query, function):
        self.__add_route(self.__post_queries, query, function)

    def add_put_route(self, query, function):
        self.__add_route(self.__put_queries, query, function)

    def add_delete_route(self, query, function):
        self.__add_route(self.__delete_queries, query, function)
    
    def page_not_found(self, httpHandler: BaseHTTPRequestHandler):
        self.write(httpHandler, 'Page if not found')

    #Properties

    @property
    def get_queries(self):
        return self.__get_queries
    
    @property
    def post_queries(self):
        return self.__post_queries
    
    @property
    def put_queries(self):
        return self.__put_queries
    
    @property
    def delete_queries(self):
        return self.__delete_queries 


    #helper methods
    def add_header(self, httpHandler: BaseHTTPRequestHandler, keyword: str, value: str):
        httpHandler.send_header(keyword, value)
        httpHandler.end_headers()

    def add_default_header(self, httpHandler: BaseHTTPRequestHandler):
        self.add_header(httpHandler, self.__CONTENT_TYPE)

    def write(self, httpHandler: BaseHTTPRequestHandler, value: Any):
        httpHandler.wfile.write(str(value).encode(self.__ENCODING))

    #Create handler with our routes
    def __create_handler(self):
        def handler_factory(rest_controller: RestController):
            class MyHandler(BaseHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    self.rest_controller = rest_controller
                    super().__init__(*args, **kwargs)

                def execure_query(self, httpHandler: BaseHTTPRequestHandler, do_queries: map) -> bool:
                    for query, func in do_queries.items():                        
                        if(httpHandler.path == query):
                            try:
                                func(self)
                            except Exception as e:
                                self.rest_controller.write(httpHandler, f"Error: 500, message: {e}")
                            return True
                    return False     

                def do_GET(self):
                    if not self.execure_query(self, self.rest_controller.get_queries):
                        rest_controller.page_not_found(self)

                def do_POST(self):
                    self.execure_query(self, self.rest_controller.post_queries)

                def do_PUT(self):
                    self.execure_query(self, self.rest_controller.put_queries)

                def do_DELETE(self):
                    self.execure_query(self, self.rest_controller.delete_queries)

            return MyHandler

        return handler_factory(self)
    
    #Run our server
    def run(self, server_class=HTTPServer):
        server_address = (self.__IP__, self.__PORT__)
        handler_class = self.__create_handler()
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()