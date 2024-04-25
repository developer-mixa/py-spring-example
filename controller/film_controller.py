from controller.utils.rest_controller import RestController
from controller.utils.mappings import RequestMapping, GetMapping, PostMapping, PutMapping, DeleteMapping
from http.server import BaseHTTPRequestHandler
from model.film_repository import FilmRepository
from model.models import Film
from view.views import films as films_view
from controller.utils.responses import OK


@RequestMapping('/films')
class FilmController(RestController):

    film_repository = FilmRepository()

    @GetMapping('/')
    def get_films(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(OK)
        self.single_header(httpHandler, 'CONTENT-TYPE', 'text/html')
        self.write(httpHandler, films_view(self.film_repository.get()))

    @PostMapping('/create')
    def add_film(self, httpHandler: BaseHTTPRequestHandler):
        film = self.get_obj_from_body(httpHandler, Film)
        film_id = self.film_repository.add(film)
        httpHandler.send_response(OK)
        self.add_default_header(httpHandler)
        self.write(httpHandler, film_id)
    
    @PutMapping('/update')
    def update_film(self, httpHandler: BaseHTTPRequestHandler):
        film = self.get_obj_from_body(httpHandler, Film)
        film_id = self.film_repository.update(film)
        httpHandler.send_response(OK)
        self.add_default_header(httpHandler)
        self.write(httpHandler, film_id)
    
    @DeleteMapping('/delete')
    def delete_film(self, httpHandler: BaseHTTPRequestHandler):
        pass