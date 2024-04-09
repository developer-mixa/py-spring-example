from model.models import Film, Base
from model.utils.db import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

class FilmRepository:

    def __init__(self) -> None:
        pass

    __engine = create_engine()

    def get_films(self) -> list[Film]:
        with Session(self.__engine) as session:
            return session.scalars(select(Film)).fetchall()
    
    def add_film(self) -> None:
        with Session(self.__engine) as session:
            return session.add()