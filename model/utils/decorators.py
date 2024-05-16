"""All decorators for comfort working with database."""


from sqlalchemy.exc import OperationalError

from model.utils.exceptions import FailConnection


def check_connection(func):
    """Check whether the connection to the database was successful.

    Args:
        func: function that you want to check

    Returns:
        wrapper: new function
    """
    def wrapper(*args, **kwargs):
        try:
            function_result = func(*args, **kwargs)
        except OperationalError:
            raise FailConnection()
        return function_result
    return wrapper
