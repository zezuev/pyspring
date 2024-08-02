from enum import Enum


class HttpMethod(Enum):
    GET = 1
    POST = 2
    UPDATE = 3
    PATCH = 4
    DELETE = 5


type URL = str
type Route = tuple[HttpMethod, URL]


class Router: ...