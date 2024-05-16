"""All decorators for comfort working with controllers."""

from controller.utils.config import MESSAGE_INTERNAL_SERVER_ERROR
from controller.utils.responses import SERVER_ERROR


def default_wrap_exceptions(func):
    """Process request for any errors by returning 500.

    Args:
        func : function that must have http_handler argument

    Returns:
        wrapper: updated function
    """
    def wrapper(self, http_handler):
        try:
            func(self, http_handler)
        except Exception:
            http_handler.send_response(SERVER_ERROR)
            self.write(http_handler, MESSAGE_INTERNAL_SERVER_ERROR)
    return wrapper
