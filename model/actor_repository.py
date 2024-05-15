"""Module for actor repository."""
from model.models import Actor
from model.utils.crud import CrudRepository
from model.utils.db import create_engine


class ActorRepository(CrudRepository):
    """Repository for working with actors."""

    _engine = create_engine()
    _model_class = Actor
