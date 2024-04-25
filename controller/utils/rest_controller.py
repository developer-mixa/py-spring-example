from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any
from view.views import main_page
from controller.utils.query_type import QueryType
from controller.utils.exceptions import PathRedefinitionException


# Controllers

class RestController:

    # Constants
    __auto_add_header__ = True
    __CONTENT_TYPE = 'Content-type'
    __TEXT_JSON = 'text/json'

    #Settings
    __BASE_URL__ = ''
    __ENCODING = 'UTF-8'

    #All queries with routes
    queries : dict[QueryType, dict[str, int]] = {}
    
    #Base init
    def __init__(self) -> None:
        self.__init_routes()

    def __init_routes(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'route_info'):
                query_type, path = attr.route_info
                self.add_route(query_type, path, attr)

    #Add-route methods

    def add_route(self, query_type: QueryType, query: str, function, autocompletion: bool=True):
        if query_type not in self.queries:
            self.queries[query_type] = {}
        if self.queries[query_type].get(self.__BASE_URL__ + query):
            raise PathRedefinitionException(query)
        self.queries[query_type][self.__BASE_URL__ + query] = function
        if autocompletion and query[len(query)-1] != '/':
            self.queries[query_type][self.__BASE_URL__ + query + '/'] = function
        elif autocompletion and query[len(query)-1] == '/':
            self.queries[query_type][self.__BASE_URL__ + query[:-1]] = function


    #helper methods
    def single_header(self, httpHandler: BaseHTTPRequestHandler, keyword: str, value: str):
        httpHandler.send_header(keyword, value)
        httpHandler.end_headers()

    def add_default_header(self, httpHandler: BaseHTTPRequestHandler):
        self.single_header(httpHandler, self.__CONTENT_TYPE, self.__TEXT_JSON)

    def write(self, httpHandler: BaseHTTPRequestHandler, value: Any):
        httpHandler.wfile.write(str(value).encode(self.__ENCODING))

    def get_obj_from_body(self, httpHandler: BaseHTTPRequestHandler, cls: Any) -> Any:
        import json
        content_length = int(httpHandler.headers['Content-Length'])
        post_data = httpHandler.rfile.read(content_length).decode(self.__ENCODING)
        return cls(**json.loads(post_data))

class GlobalRestController:
    
    __ENCODING = 'UTF-8'

    def __init__(self, ip, port,controllers: list[RestController] | tuple[RestController]) -> None:
        self.__ip = ip
        self.__port = port
        self.__controllers = controllers
        self.__fill_queries()

    def __fill_queries(self):
        self.__all_queries = {}
        for controller in self.__controllers:
            for path, function in controller.queries.items():
                self.__all_queries[path] = function
        

    def default_page(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        httpHandler.send_header('Content-type', 'text/html')
        httpHandler.end_headers()
        httpHandler.wfile.write(main_page().encode(self.__ENCODING))


    def __create_handler(self):
            def handler_factory(all_queries, globalController: GlobalRestController) -> BaseHTTPRequestHandler:
                class MyHandler(BaseHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        self.all_queries, self.global_controller = all_queries, globalController
                        super().__init__(*args, **kwargs)

                    def execure_query(self, httpHandler: BaseHTTPRequestHandler, do_queries: map) -> bool:
                        for query, func in do_queries.items():                        
                            if(httpHandler.path == query):
                                func(self)
                                return True
                        return False     

                    def do_GET(self):
                        if not self.execure_query(self, self.all_queries[QueryType.GET]):
                            globalController.default_page(self)

                    def do_POST(self):
                        self.execure_query(self, self.all_queries[QueryType.POST])

                    def do_PUT(self):
                        self.execure_query(self, self.all_queries[QueryType.PUT])

                    def do_DELETE(self):
                        self.execure_query(self, self.all_queries[QueryType.DELETE])

                return MyHandler

            return handler_factory(self.__all_queries, self)
        
    def run(self, server_class=HTTPServer):
        server_address = (self.__ip, self.__port)
        handler_class = self.__create_handler()
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()        