"""Main file."""
from controller.actor_controller import ActorController
from controller.film_controller import FilmController
from controller.utils.rest_controller import GlobalRestController

from dotenv import load_dotenv
from os import getenv

load_dotenv()

port = int(getenv('SERVER_PORT', 8000))
ip = getenv('SERVER_HOST', 'localhost')

app = GlobalRestController(
controllers=[
    FilmController(),
    ActorController(),
    ],
)

def run(*args):
    app.run(ip=ip, port=port)


if __name__ == '__main__':
    run()
