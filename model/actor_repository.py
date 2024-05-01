from model.utils.crud import CrudRepository
from model.models import Actor
from model.utils.db import create_engine

class ActorRepository(CrudRepository):
    _engine = create_engine()
    _model_class = Actor