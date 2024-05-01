from controller.utils.rest_controller import RestController
from controller.utils.mappings import RequestMapping, GetMapping, PostMapping, PutMapping, DeleteMapping
from http.server import BaseHTTPRequestHandler
from model.actor_repository import ActorRepository
from controller.utils.responses import OK, CREATED
from view.views import actors as actors_view
from model.models import Actor

@RequestMapping('/actors')
class ActorController(RestController):

    actor_repository = ActorRepository()

    @GetMapping('/')
    def get_films(self, httpHandler: BaseHTTPRequestHandler):
        httpHandler.send_response(OK)
        self.single_header(httpHandler, 'CONTENT-TYPE', 'text/html')
        self.write(httpHandler, actors_view(self.actor_repository.get()))

    @PostMapping('/create')
    def add_actor(self, httpHandler: BaseHTTPRequestHandler):
        actor = self.get_obj_from_body(httpHandler, Actor)
        actor_id = self.actor_repository.add(actor)
        httpHandler.send_response(CREATED)
        self.add_default_header(httpHandler)
        self.write(httpHandler, actor_id)
    
    @PutMapping('/update')
    def update_actor(self, httpHandler: BaseHTTPRequestHandler):
        actor = self.get_obj_from_body(httpHandler, Actor)
        actor_id = self.actor_repository.update(actor)
        httpHandler.send_response(OK)
        self.add_default_header(httpHandler)
        self.write(httpHandler, actor_id)
    
    @DeleteMapping('/delete')
    def delete_film(self, httpHandler: BaseHTTPRequestHandler):
        pass