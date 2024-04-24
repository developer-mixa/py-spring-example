from controller.utils.rest_controller import RestController
from controller.utils.query_type import QueryType
from http.server import BaseHTTPRequestHandler
from model.film_repository import FilmRepository
from model.models import Film

class ActorController(RestController):

    __BASE_URL__ = '/actors'

    def init_routes(self):
        self.add_route(QueryType.GET, '/', self.get_actors)

    def get_actors(self, httpHandler: BaseHTTPRequestHandler):
        self.write(httpHandler, 'actors')
        