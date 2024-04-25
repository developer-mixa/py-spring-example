from controller.utils.rest_controller import RestController
from controller.utils.mappings import RequestMapping, GetMapping
from controller.utils.query_type import QueryType
from http.server import BaseHTTPRequestHandler

@RequestMapping('/actors')
class ActorController(RestController):

    @GetMapping('/')
    def get_actors(self, httpHandler: BaseHTTPRequestHandler):
        self.write(httpHandler, 'actors')