from controller.film_controller import FilmController
from controller.actor_controller import ActorController
from controller.utils.rest_controller import GlobalRestController

globalRestController = GlobalRestController(
    ip='',
    port=8000,
    controllers=[
        FilmController(),
        ActorController()
    ]
)

globalRestController.run()