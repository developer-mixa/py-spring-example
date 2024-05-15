"""Main file."""
from controller.actor_controller import ActorController
from controller.film_controller import FilmController
from controller.utils.rest_controller import GlobalRestController

PORT = 8000

global_controller = GlobalRestController(
    ip='',
    port=PORT,
    controllers=[
        FilmController(),
        ActorController(),
    ],
)

global_controller.run()
