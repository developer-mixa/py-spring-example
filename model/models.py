"""Module for database models."""

from uuid import UUID

from sqlalchemy import CheckConstraint, Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from model.utils.uuid_mixin import UUIDMixin


class Base(DeclarativeBase):
    """Base class for tables."""

    pass


class Film(UUIDMixin, Base):
    """Films table."""

    __tablename__ = 'film'

    name: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(1024))
    rating: Mapped[float] = mapped_column(Float)

    actors: Mapped[list['Actor']] = relationship('Actor', secondary='film_to_actor', back_populates='films')

    def __str__(self) -> str:
        return f'name={self.name}, description={self.description}, rating={self.rating}'

    __table_args__ = (
        CheckConstraint('LENGTH(name) > 0'),
        CheckConstraint('LENGTH(description) > 0'),
        CheckConstraint('rating >= 0'),
    )


class Actor(UUIDMixin, Base):
    """Actors table."""

    __tablename__ = 'actor'

    name: Mapped[str] = mapped_column(String(128))
    surname: Mapped[str] = mapped_column(String(128))
    age: Mapped[int]

    films: Mapped[list[Film]] = relationship('Film', secondary='film_to_actor', back_populates='actors')

    __table_args__ = (
        CheckConstraint('LENGTH(name) > 0'),
        CheckConstraint('LENGTH(surname) > 0'),
        CheckConstraint('age >= 0'),
    )


class FilmActor(UUIDMixin, Base):
    """Assoative many-to-many table for films and actors."""

    __tablename__ = 'film_to_actor'

    film_id: Mapped[UUID] = mapped_column(ForeignKey('film.id'))
    actor_id: Mapped[UUID] = mapped_column(ForeignKey('actor.id'))
