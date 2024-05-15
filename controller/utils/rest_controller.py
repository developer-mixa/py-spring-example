from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable, ClassVar
from uuid import UUID

from controller.utils.config import (CONTENT_TEXT_HTML, CONTENT_TEXT_JSON,
                                     CONTENT_TYPE, UTF_8)
from controller.utils.exceptions import PathRedefinitionException
from controller.utils.mappings import (DeleteMapping, GetMapping, PostMapping,
                                       PutMapping)
from controller.utils.query_type import QueryType
from controller.utils.responses import (CREATED, NO_CONTENT, NOT_FOUND, OK,
                                        SERVER_ERROR)
from model.utils.crud import CrudRepository
from model.utils.exceptions import NotFound
from view.views import main_page

# Controllers

class RestController:

    # Constants
    __auto_add_header__ = True

    #Settings
    __BASE_URL__ = ''

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
        self.single_header(httpHandler, CONTENT_TYPE, CONTENT_TEXT_JSON)

    def write(self, httpHandler: BaseHTTPRequestHandler, value: Any):
        httpHandler.wfile.write(str(value).encode(UTF_8))

    def get_request(self, httpHandler: BaseHTTPRequestHandler, key: str):
        import json
        content_length = int(httpHandler.headers['Content-Length'])
        data = httpHandler.rfile.read(content_length).decode(UTF_8)
        return json.loads(data)[key]

    def get_obj_from_body(self, httpHandler: BaseHTTPRequestHandler, cls: Any) -> Any:
        import json
        content_length = int(httpHandler.headers['Content-Length'])
        data = httpHandler.rfile.read(content_length).decode(UTF_8)
        return cls(**json.loads(data))


class GlobalRestController:
    """The main controller, which essentially glues all the other controllers into one.

    Example usage:
        >>> GlobalRestController(
        >>> ip='',
        >>> port=PORT,
        >>> controllers=[
            >>> StudentController(),
            >>> TeacherController(),
        >>> ],
        >>> ).run()

    """

    def __init__(self, ip: str, port: int, controllers: list[RestController]) -> None:
        """Init of global rest controller.

        Args:
            ip (str): The most based ip url
            port (int): Port for the server
            controllers (list[RestController]): all your controllers
        """
        self.__ip = ip
        self.__port = port
        self.__controllers = controllers
        self.__fill_queries()

    def default_page(self, http_handler: BaseHTTPRequestHandler):
        """Show default page in the site.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
        """
        http_handler.send_response(OK)
        http_handler.send_header(CONTENT_TYPE, CONTENT_TEXT_HTML)
        http_handler.end_headers()
        http_handler.wfile.write(main_page().encode(UTF_8))

    def run(self, server_class=HTTPServer):
        """Run server with putted ip and port.

        Args:
            server_class: class which serve our server.
        """
        server_address = (self.__ip, self.__port)
        handler_class = self.__create_handler()
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

    def __fill_queries(self):
        self.__all_queries = {}
        for controller in self.__controllers:
            for path, function in controller.queries.items():
                self.__all_queries[path] = function

    def __create_handler(rest_self):
        def handler_factory(queries, global_controller: GlobalRestController) -> BaseHTTPRequestHandler:
            class HttpHandler(BaseHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    self.queries, self.global_controller = queries, global_controller
                    super().__init__(*args, **kwargs)

                def execure_query(self, do_queries: map) -> bool:
                    for query, func in do_queries.items():
                        if self.path == query:
                            func(self)
                            return True
                    return False

                def do_GET(self):
                    if not self.execure_query(self.queries[QueryType.GET]):
                        global_controller.default_page(self)

                def do_POST(self):
                    self.execure_query(self.queries[QueryType.POST])

                def do_PUT(self):
                    self.execure_query(self.queries[QueryType.PUT])

                def do_DELETE(self):
                    self.execure_query(self.queries[QueryType.DELETE])

            return HttpHandler

        return handler_factory(rest_self.__all_queries, rest_self)


class SimpleRestController(RestController):
    """Simple controller for quickly creating a controller that uses only crud methods.

    Needs to be redefined:
        model_class: Class for which crud methods will be created
        crud_repository: Class that must be inherited from the CrudRepository
        get_view: A function that will be returned in a get request based
        on the data that get returns from the crud repository
        It must take a controller as arguments,
        and the second argument is a list of your entities
        for example: def person_view(_, persons: list): pass

    Example:
        @RequestMapping('/persons')
        class ActorController(SimpleRestController):
            model_class = Person
            crud_repository = PersonRepository()
            get_view = person_view
    """

    model_class: ClassVar
    crud_repository: CrudRepository
    get_view: Callable

    @GetMapping('/')
    def get(self, http_handler: BaseHTTPRequestHandler):
        """Get all model classes from database.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
        """
        http_handler.send_response(OK)
        self.single_header(http_handler, CONTENT_TYPE, CONTENT_TEXT_HTML)
        self.write(http_handler, self.get_view(self.crud_repository.get()))

    @PostMapping('/create')
    def add(self, http_handler: BaseHTTPRequestHandler):
        """Add model class in database.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
        """
        film = self.get_obj_from_body(http_handler, self.model_class)
        film_id = self.crud_repository.add(film)
        http_handler.send_response(CREATED)
        self.add_default_header(http_handler)
        self.write(http_handler, film_id)

    @PutMapping('/update')
    def update(self, http_handler: BaseHTTPRequestHandler):
        """Update model class in database.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
        """
        film = self.get_obj_from_body(http_handler, self.model_class)
        film_id = self.crud_repository.update(film)
        http_handler.send_response(OK)
        self.add_default_header(http_handler)
        self.write(http_handler, film_id)

    @DeleteMapping('/delete')
    def delete(self, http_handler: BaseHTTPRequestHandler):
        """Delete model class in database by id.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
        """
        response = SERVER_ERROR
        try:
            self.crud_repository.remove(UUID(self.get_request(http_handler, 'id')))
        except NotFound:
            response = NOT_FOUND
        except Exception:
            response = SERVER_ERROR
        else:
            response = NO_CONTENT
        finally:
            http_handler.send_response(response)
            self.add_default_header(http_handler)
