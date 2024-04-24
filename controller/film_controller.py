from controller.utils.rest_controller import RestController
from controller.utils.query_type import QueryType
from http.server import BaseHTTPRequestHandler
from model.film_repository import FilmRepository
from model.models import Film


class FilmController(RestController):

    __BASE_URL__ = '/films'

    film_repository = FilmRepository()

    def init_routes(self):
        self.add_route(QueryType.GET, '/', self.get_films)
        self.add_route(QueryType.POST, '/create', self.add_film)
    
    def get_films(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        self.add_default_header(httpHandler)
        self.write(httpHandler, "something")

    def add_film(self, httpHandler: BaseHTTPRequestHandler):
        film = self.get_obj_from_body(httpHandler, Film)
        film_id = self.film_repository.add_film(film)
        httpHandler.send_response(200)
        self.add_default_header()
        self.write(httpHandler, film_id)
