class FilmNotFound(Exception):
    def __init__(self) -> None:
        super().__init__('Film was not found!')