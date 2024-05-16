"""Module for project exceptions."""


class PathRedefinitionException(Exception):
    """Class that is called when duplicating paths to request."""

    def __init__(self, path: str) -> None:
        """Init path redefinition.

        Args:
            path (str): path to request
        """
        super().__init__(f'There was a double path definition along this path: {path}')
