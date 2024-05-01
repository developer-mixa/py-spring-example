class NotFound(Exception):
    def __init__(self, class_) -> None:
        super().__init__(f'{str(class_)} was not found!')