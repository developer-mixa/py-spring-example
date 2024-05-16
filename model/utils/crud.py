"""Model with CrudRepository."""
from uuid import UUID

from sqlalchemy import Engine, select, text
from sqlalchemy.orm import Session

from model.utils.decorators import check_connection
from model.utils.exceptions import NotFound


class CrudRepository:
    """Base class that implements KRUD for the database.

    Example:
        class PersonRepository(CrudRepository):
            _engine = your_engine()
            _model_class = Person
    """

    _engine: Engine
    _model_class: type

    @check_connection
    def get(self) -> list[type]:
        """Get all model class objects.

        Returns:
            list[type]: All model class objects
        """
        with Session(self._engine) as session:
            return session.scalars(select(self._model_class)).fetchall()

    @check_connection
    def add(self, model_class: type) -> UUID:
        """Add model class to database.

        Args:
            model_class (type): Model class which we need to add

        Returns:
            UUID: Added object id
        """
        with Session(self._engine) as session:
            session.add(model_class)
            session.commit()
            return model_class.id

    @check_connection
    def update(self, updated_model_class: type) -> UUID:
        """Update object by Updated class.

        Args:
            updated_model_class (type): Model database class

        Raises:
            NotFound: Raise when object with this id is not found

        Returns:
            UUID: Updated object id
        """
        with Session(self._engine) as session:
            table_name = self._model_class.__tablename__
            query = text(f'SELECT * FROM {table_name} WHERE id = :id')
            model_str = session.execute(query, {'id': updated_model_class.id}).fetchone()
            model = self._model_class(**model_str._asdict())
            if not model:
                raise NotFound(self._model_class)
            for attr, attr_value in vars(updated_model_class).items():
                setattr(model, attr, attr_value)
            session.merge(model)
            session.commit()
            return model.id

    @check_connection
    def remove(self, model_id: UUID):
        """Remove object by id.

        Args:
            model_id (UUID): Object id which we need to delete

        Raises:
            NotFound: Raise when object with this id is not found
        """
        with Session(self._engine) as session:
            table_name = self._model_class.__tablename__
            query = text(f'DELETE FROM {table_name} WHERE id = :id')
            removed_id = session.execute(query, {'id': model_id})
            session.commit()
            if removed_id.rowcount == 0:
                raise NotFound(self._model_class)
