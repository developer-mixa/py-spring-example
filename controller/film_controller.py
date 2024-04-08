from controller.utils.rest_controller import RestController
from http.server import BaseHTTPRequestHandler
from model.film_repository import FilmRepository

class FilmController(RestController):

    __BASE_URL__ = '/films'

    film_repository = FilmRepository()

    def init_routes(self):
        self.add_get_route('/', self.get_films)
    
    def get_films(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        self.write(httpHandler, self.film_repository.get_films())