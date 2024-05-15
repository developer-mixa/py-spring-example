"""All exception in model layer."""


class NotFound(Exception):
    """Exception when there is no model class in database."""

    def __init__(self, model_class: type) -> None:
        """Init NotFound exception.

        Args:
            model_class : Database model
        """
        class_name = str(model_class)
        super().__init__(f'{class_name} was not found!')
