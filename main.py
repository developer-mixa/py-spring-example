"""Main file."""
from os import getenv

from dotenv import load_dotenv

from controller.actor_controller import ActorController
from controller.film_controller import FilmController
from controller.utils.rest_controller import GlobalRestController

load_dotenv()

DEFAULT_PORT = 8000
DEFAULT_HOST = 'localhost'

port = int(getenv('SERVER_PORT', DEFAULT_PORT))
ip = getenv('SERVER_HOST', DEFAULT_HOST)

app = GlobalRestController(
    ip=ip,
    port=port,
    controllers=[
        FilmController(),
        ActorController(),
    ],
)


if __name__ == '__main__':
    app.run()
