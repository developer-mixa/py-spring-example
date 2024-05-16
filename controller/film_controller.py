"""Module for film controller."""


from controller.utils.mappings import RequestMapping
from controller.utils.rest_controller import SimpleRestController
from model.film_repository import FilmRepository
from model.models import Film
from view.views import films as films_view


@RequestMapping('/films')
class FilmController(SimpleRestController):
    """Controller for working with films."""

    crud_repository = FilmRepository()
    model_class = Film
    get_view = films_view
