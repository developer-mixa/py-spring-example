from controller.utils.rest_controller import SimpleRestController
from controller.utils.mappings import RequestMapping
from model.actor_repository import ActorRepository
from view.views import actors as actors_view
from model.models import Actor

@RequestMapping('/actors')
class ActorController(SimpleRestController):
    model_class = Actor
    crud_repository = ActorRepository()
    get_view = actors_view
