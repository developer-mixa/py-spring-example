"""Module for actor controller."""


from controller.utils.mappings import RequestMapping
from controller.utils.rest_controller import SimpleRestController
from model.actor_repository import ActorRepository
from model.models import Actor
from view.views import actors as actors_view


@RequestMapping('/actors')
class ActorController(SimpleRestController):
    """Controller for working with actors."""

    model_class = Actor
    crud_repository = ActorRepository()
    get_view = actors_view
