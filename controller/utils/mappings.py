"""Module for different query mappings."""


from controller.utils.query_type import QueryType


class RequestMapping:
    """Class for setting the path to the controller.

    Important:
        the class must be inherited from RestController

    Example usage:
    >>> @RequestMapping('/persons')
    >>> class PersonController(RestController):
    """

    def __init__(self, path: str):
        """Init request mapping.

        Args:
            path (str): path to the controller
        """
        self.path = path

    def __call__(self, controller):
        """Assign the base url to the passed path from the controller.

        Args:
            controller (RestController): your rest controller

        Returns:
            RestController: Updated rest controller
        """
        controller.__base_url__ = self.path
        return controller


class __BaseMapping:
    def __init__(self, path, query_type):
        self.path = path
        self.query_type = query_type

    def __call__(self, func):
        func.route_info = (self.query_type, self.path)
        return func


class GetMapping(__BaseMapping):
    """Class to designate a function as a get request.

    Important:
        the function must take http_handler as arguments

    Example usage:
    >>> @GetMapping('/get')
    >>> def get(self, http_handler: BaseHTTPRequestHandler):
    >>>     pass
    """

    def __init__(self, path):
        """Init mapping for get query.

        Args:
            path (str): path for this query
        """
        super().__init__(path, QueryType.GET)


class PostMapping(__BaseMapping):
    """Class to designate a function as a post request.

    Important:
        the function must take http_handler as arguments

    Example usage:
    >>> @PostMapping('/create')
    >>> def create(self, http_handler: BaseHTTPRequestHandler):
    >>>     pass
    """

    def __init__(self, path):
        """Init mapping for post query.

        Args:
            path (str): path for this query
        """
        super().__init__(path, QueryType.POST)


class PutMapping(__BaseMapping):
    """Class to designate a function as a put request.

    Important:
        the function must take http_handler as arguments

    Example usage:
    >>> @PutMapping('/update')
    >>> def update(self, http_handler: BaseHTTPRequestHandler):
    >>>     pass

    """

    def __init__(self, path):
        """Init mapping for put query.

        Args:
            path (str): path for this query
        """
        super().__init__(path, QueryType.PUT)


class DeleteMapping(__BaseMapping):
    """Class to designate a function as a delete request.

    Important:
        the function must take http_handler as arguments

    Example usage:
    >>> @DeleteMapping('/delete')
    >>> def delete(self, http_handler: BaseHTTPRequestHandler):
    >>>     pass
    """

    def __init__(self, path: str):
        """Init mapping for delete query.

        Args:
            path (str): path for this query
        """
        super().__init__(path, QueryType.DELETE)
