"""Module for film repository."""

from model.models import Film
from model.utils.crud import CrudRepository
from model.utils.db import create_engine


class FilmRepository(CrudRepository):
    """Repository for working with films."""

    _engine = create_engine()
    _model_class = Film
