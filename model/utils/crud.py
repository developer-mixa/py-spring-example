from typing import Any
from abc import abstractmethod
from sqlalchemy import Engine, select, delete
from sqlalchemy.orm import Session
from model.utils.exceptions import FilmNotFound
from uuid import UUID
from sqlalchemy import text

class CrudRepository:

    _engine: Engine
    _model_class: Any

    def get(self) -> list[Any]:
        with Session(self._engine) as session:
            return session.scalars(select(self._model_class)).fetchall()
    
    def add(self, model_class: Any) -> None:
        with Session(self._engine) as session:
            session.add(model_class)
            session.commit()
            return model_class.id
    
    def update(self, updated_model_class: Any):
        with Session(self._engine) as session:
            table_name = self._model_class.__tablename__
            query = text(f"SELECT * FROM {table_name} WHERE id = :id")
            model_str = session.execute(query, {"id" : updated_model_class.id}).fetchone()
            model = self._model_class(**model_str._asdict())
            if not model:
                raise FilmNotFound()
            for attr, value in vars(updated_model_class).items():
                if hasattr(model, attr):
                    setattr(model, attr, value)  
            session.merge(model)         
            session.commit()
            return model.id
    
    def remove(self, id: UUID):
        with Session(self._engine) as session:
            deleted_film = session.scalar(delete(self._model_class).where(id=id))
            return deleted_film.id    