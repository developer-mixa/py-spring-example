from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any
from view.views import main_page
from typing import Callable
from controller.utils.query_type import QueryType


class RestController:

    # Constants
    __ENCODING = 'UTF-8'
    __auto_add_header__ = True
    __CONTENT_TYPE = 'Content-type'
    __TEXT_JSON = 'text/json'

    #Settings
    __BASE_URL__ = ''

    #All queries with routes
    queries : dict[QueryType, dict[str, int]] = {}
    
    #Base init
    def __init__(self) -> None:
        self.init_routes()

    def init_routes(self):
        pass

    #Add-route methods

    def add_route(self, query_type: QueryType, query, function):
        self.queries[query_type] = {self.__BASE_URL__ + query: function}
    
    def default_page(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        httpHandler.send_header('Content-type', 'text/html')
        httpHandler.end_headers()
        httpHandler.wfile.write(main_page().encode(self.__ENCODING))

    #Properties
    
    #helper methods
    def add_header(self, httpHandler: BaseHTTPRequestHandler, keyword: str, value: str):
        httpHandler.send_header(keyword, value)
        httpHandler.end_headers()

    def add_default_header(self, httpHandler: BaseHTTPRequestHandler):
        self.add_header(httpHandler, self.__CONTENT_TYPE, self.__TEXT_JSON)

    def write(self, httpHandler: BaseHTTPRequestHandler, value: Any):
        httpHandler.wfile.write(str(value).encode(self.__ENCODING))

    def get_obj_from_body(self, httpHandler: BaseHTTPRequestHandler, cls: Any) -> Any:
        import json
        content_length = int(httpHandler.headers['Content-Length'])
        post_data = httpHandler.rfile.read(content_length).decode(self.__ENCODING)
        return cls(**json.loads(post_data))

class GlobalRestController:
    
    def __init__(self, ip, port,controllers: list[RestController] | tuple[RestController]) -> None:
        self.__ip = ip
        self.__port = port
        self.__controllers = controllers


    def __create_handler(self):
            def handler_factory(rest_controllers: list[RestController]) -> BaseHTTPRequestHandler:
                class MyHandler(BaseHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        self.rest_controllers = rest_controllers
                        super().__init__(*args, **kwargs)

                    def execure_query(self, httpHandler: BaseHTTPRequestHandler, do_queries: map) -> bool:
                        for query, func in do_queries.items():                        
                            if(httpHandler.path == query):
                                func(self)
                                return True
                        return False     

                    def do_GET(self):
                        for rest_controller in self.rest_controllers:
                            if not self.execure_query(self, rest_controller.queries[QueryType.GET]):
                                rest_controller.default_page(self)

                    def do_POST(self):
                        for rest_controller in self.rest_controllers:
                            self.execure_query(self, rest_controller.queries[QueryType.POST])

                    def do_PUT(self):
                        for rest_controller in self.rest_controllers:
                            self.execure_query(self, rest_controller.queries[QueryType.PUT])

                    def do_DELETE(self):
                        for rest_controller in self.rest_controllers:
                            self.execure_query(self, rest_controller.queries[QueryType.DELETE])

                return MyHandler

            return handler_factory(self.__controllers)
        
    def run(self, server_class=HTTPServer):
        server_address = (self.__ip, self.__port)
        handler_class = self.__create_handler()
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()        