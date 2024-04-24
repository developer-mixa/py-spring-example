class PathRedefinitionException(Exception):
    def __init__(self, query: str) -> None:
        super().__init__(f'There was a double path definition along this path: {query}')