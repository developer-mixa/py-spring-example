from model.models import Film, Base
from model.utils.db import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from model.utils.exceptions import FilmNotFound

class FilmRepository:

    def __init__(self) -> None:
        pass

    __engine = create_engine()

    def get_films(self) -> list[Film]:
        with Session(self.__engine) as session:
            return session.scalars(select(Film)).fetchall()
    
    def add_film(self, film: Film) -> None:
        with Session(self.__engine) as session:
            session.add(film)
            session.commit()
            return film.id
    
    def update_film(self, updated_film: Film):
        with Session(self.__engine) as session:
            film: Film = session.scalar(select(Film).where(id=updated_film.id))
            if not film:
                raise FilmNotFound()
            film.name = updated_film.name
            film.description = updated_film.description
            film.rating = updated_film.rating
            session.commit()
            return film.id