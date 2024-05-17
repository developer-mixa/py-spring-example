"""Module for different rest controllers."""


import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable, ClassVar, Optional
from uuid import UUID

from controller.utils.config import (CONTENT_LENGHT, CONTENT_TEXT_HTML,
                                     CONTENT_TEXT_JSON, CONTENT_TYPE, UTF8)
from controller.utils.decorators import default_wrap_exceptions
from controller.utils.exceptions import PathRedefinitionException
from controller.utils.mappings import (DeleteMapping, GetMapping, PostMapping,
                                       PutMapping)
from controller.utils.query_type import QueryType
from controller.utils.responses import (CREATED, NO_CONTENT, NOT_FOUND, OK,
                                        SERVER_ERROR)
from model.utils.crud import CrudRepository
from model.utils.exceptions import NotFound
from view.views import main_page


class RestController:
    """class in which we can process requests.

    Example usage:
    >>> class PersonController(RestController):

        >>> person_repository = PersonRepository()

        >>> @GetMapping('/')
        >>> def get(self, http_handler: BaseHTTPRequestHandler):
            >>> http_handler.send_response(OK)
            >>> self.single_header(http_handler, CONTENT_TYPE, CONTENT_TEXT_HTML)
            >>> self.write(http_handler, person_view(person_repository.get_persons()))

        >>> @PostMapping('/create')
        >>> def add(self, http_handler: BaseHTTPRequestHandler):
            >>> person = self.get_obj_from_body(http_handler, Person)
            >>> person_id = self.person.add(person)
            >>> http_handler.send_response(CREATED)
            >>> self.add_default_header(http_handler)
            >>> self.write(http_handler, person_id)

        >>> @PutMapping('/update')
        >>> def update(self, http_handler: BaseHTTPRequestHandler):
            >>> person = self.get_obj_from_body(http_handler, Person)
            >>> person_id = self.crud_repository.update(person)
            >>> http_handler.send_response(OK)
            >>> self.add_default_header(http_handler)
            >>> self.write(http_handler, person_id)

        >>> @DeleteMapping('/delete')
        >>> def delete(self, http_handler: BaseHTTPRequestHandler):
            >>> response = SERVER_ERROR
            >>> try:
                >>> self.person_repository.remove(UUID(self.get_request(http_handler, 'id')))
            >>> except NotFound:
                >>> response = NOT_FOUND
            >>> except Exception:
                >>> response = SERVER_ERROR
            >>> else:
                >>> response = NO_CONTENT
            >>> finally:
                >>> http_handler.send_response(response)
                >>> self.add_default_header(http_handler)

    Without mappings:
    >>> def __init__(self):
        >>> self.add_route(QueryType.GET, '/', get)
        >>> self.add_route(QueryType.POST, '/create', add)
        >>> self.add_route(QueryType.UPDATE, '/update', update)
        >>> self.add_route(QueryType.DELETE, '/delete', delete)
        >>> super.init()
    """

    __auto_add_header__ = True

    __base_url__ = ''

    queries: dict[QueryType, dict[str, int]] = {}

    def __init__(self) -> None:
        """Init routes that can be dynamically added using mappings."""
        self.__init_routes()

    def add_route(self, query_type: QueryType, query: str, function, autocompletion: Optional[bool] = True):
        """Add route by query type with your query and put function there.

        Args:
            query_type (QueryType): query type
            query (str): query
            function (_type_): function which will call by query
            autocompletion (Optional[bool]): adds at the end / if it's not there. Default true

        Raises:
            PathRedefinitionException: _description_
        """
        if query_type not in self.queries:
            self.queries[query_type] = {}
        last_query_sym = query[-1]
        result_query = self.__base_url__ + query
        if autocompletion and last_query_sym != '/':
            result_query = f'{self.__base_url__}{query}/'
        if self.queries[query_type].get(result_query):
            raise PathRedefinitionException(result_query)
        self.queries[query_type][result_query] = function
    # helper methods

    def single_header(self, http_handler: BaseHTTPRequestHandler, keyword: str, writed_value: str):
        """Add the only header with key = keyword and value = writed_value.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
            keyword (str): header key
            writed_value (str): header_value
        """
        http_handler.send_header(keyword, writed_value)
        http_handler.end_headers()

    def add_default_header(self, http_handler: BaseHTTPRequestHandler):
        """Add the only content type which equals json.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
        """
        self.single_header(http_handler, CONTENT_TYPE, CONTENT_TEXT_JSON)

    def write(self, http_handler: BaseHTTPRequestHandler, writed_value: Any):
        """Write data to wfile.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
            writed_value (Any): value which you want to write
        """
        http_handler.wfile.write(str(writed_value).encode(UTF8))

    def get_request(self, http_handler: BaseHTTPRequestHandler, key: str) -> Any:
        """Get request by key.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
            key (str): key to your model

        Returns:
            Any: value from the request
        """
        content_length = self.__get_content_legth(http_handler)
        decode_data = http_handler.rfile.read(content_length).decode(UTF8)
        return json.loads(decode_data)[key]

    def get_obj_from_body(self, http_handler: BaseHTTPRequestHandler, model_class: type) -> type:
        """Get model class from request body.

        Args:
            http_handler (BaseHTTPRequestHandler): your http handler
            model_class: model class which you want to get

        Returns:
            type: your model class from request
        """
        content_length = self.__get_content_legth(http_handler)
        return model_class(**json.loads(http_handler.rfile.read(content_length).decode(UTF8)))

    def __get_content_legth(self, http_handler: BaseHTTPRequestHandler):
        return int(http_handler.headers[CONTENT_LENGHT])

    def __init_routes(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'route_info'):
                query_type, path = attr.route_info
                self.add_route(query_type, path, attr)


class GlobalRestController:
    """The main controller, which essentially glues all the other controllers into one.

    Example usage:
        >>> GlobalRestController(
        >>> ip=localhost,
        >>> port=8080,
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
        self.__ip__ = ip
        self.__port__ = port
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
        http_handler.wfile.write(main_page().encode(UTF8))

    def run(self, server_class=HTTPServer):
        """Run server with putted ip and port.

        Args:
            server_class: class which serve our server.
        """
        server_address = (self.__ip__, self.__port__)
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
    @default_wrap_exceptions
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
        response = OK
        try:
            film_id = self.crud_repository.update(film)
        except NotFound:
            response = NOT_FOUND
        except Exception:
            response = SERVER_ERROR
        else:
            self.add_default_header(http_handler)
            self.write(http_handler, film_id)
        finally:
            http_handler.send_response(response)

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
