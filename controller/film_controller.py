from controller.utils.rest_controller import RestController
from controller.utils.mappings import RequestMapping, GetMapping, PostMapping, PutMapping, DeleteMapping
from http.server import BaseHTTPRequestHandler
from model.film_repository import FilmRepository
from model.models import Film
from view.views import films as films_view
from controller.utils.responses import OK, CREATED, NOT_FOUND, NO_CONTENT, SERVER_ERROR
from uuid import UUID
from model.utils.exceptions import NotFound

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
        httpHandler.send_response(CREATED)
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
        try:
            self.film_repository.remove(UUID(self.get_request(httpHandler, 'id')))
            httpHandler.send_response(NO_CONTENT)
            self.add_default_header(httpHandler)
        except NotFound:
            httpHandler.send_response(NOT_FOUND)
            self.add_default_header(httpHandler)
        except Exception as e:
            print(e)
            httpHandler.send_response(SERVER_ERROR)
            self.add_default_header(httpHandler)
