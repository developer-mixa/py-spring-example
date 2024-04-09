from controller.utils.rest_controller import RestController
from http.server import BaseHTTPRequestHandler
from model.film_repository import FilmRepository

class FilmController(RestController):

    __BASE_URL__ = '/films'

    film_repository = FilmRepository()

    def init_routes(self):
        self.add_get_route('/', self.get_films)
        self.add_post_route('/create', self.add_film)
    
    def get_films(self, httpHandler: BaseHTTPRequestHandler):
        self.write(httpHandler, self.film_repository.get_films())
        httpHandler.send_response(200)

    def add_film(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(200)
        content_length = int(httpHandler.headers['Content-Length'])
        post_data = httpHandler.rfile.read(content_length)
        print(post_data)