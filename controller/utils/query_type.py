"""Module for rest query types."""


from enum import Enum


class QueryType(Enum):
    """Class for recognizing API requests."""

    GET = 'GET'

    POST = 'POST'

    PUT = 'PUT'

    DELETE = 'DELETE'
