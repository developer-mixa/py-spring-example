from model.models import Film
from model.utils.db import create_engine
from model.utils.crud import CrudRepository

class FilmRepository(CrudRepository):
    _engine = create_engine()
    _model_class = Film