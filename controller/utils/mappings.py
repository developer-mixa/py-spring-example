from functools import wraps
from controller.utils.query_type import QueryType

class RequestMapping:
    def __init__(self, path):
        self.path = path

    def __call__(self, cls):
        cls.__BASE_URL__ = self.path
        return cls
    
class __BaseMapping:
    def __init__(self, path, query_type):
        self.path = path
        self.query_type = query_type

    def __call__(self, func):
        func.route_info = (self.query_type, self.path)
        return func

class GetMapping(__BaseMapping):
    def __init__(self, path):
        super().__init__(path, QueryType.GET)

class PostMapping(__BaseMapping):
    def __init__(self, path):
        super().__init__(path, QueryType.POST)

class PutMapping(__BaseMapping):
    def __init__(self, path):
        super().__init__(path, QueryType.PUT)

class DeleteMapping(__BaseMapping):
    def __init__(self, path):
        super().__init__(path, QueryType.DELETE)
