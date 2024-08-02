from typing import Callable, Any
from enum import Enum


class HttpMethod(Enum):
    GET = 1
    POST = 2
    UPDATE = 3
    PATCH = 4
    DELETE = 5


type URL = str
type Function = tuple[HttpMethod, Callable]
type Request = tuple[HttpMethod, URL]


class Router:

    def __init__(self):
        self._class_functions: dict[type, set[Function]] = {}
        self._class_by_name: dict[str, type] = {}
        self._function_class: dict[Callable, str] = {}
        self._mapping: dict[Request, Callable] = {}
        self._assigned: set[Callable] = set()

    def process(self, request: Request, component: Any) -> Any:
        return self._mapping[request](component)

    def get_component_type(self, request: Request) -> type:
        f = self._mapping[request]
        class_name = self._function_class[f]
        return self._class_by_name[class_name]

    def register_function(
            self,
            method: HttpMethod,
            func: Callable,
            url: str | None = None,
    ):
        class_name = self.get_function_class(func)
        self._class_functions.setdefault(class_name, set()).add((method, func))
        self._function_class[func] = class_name
        if url:
            self._mapping[(method, url)] = func
            self._assigned.add(func)

    def register_class[T](self, t: type[T], url: str | None = None):
        class_name = t.__name__
        if url:
            if any(f in self._assigned for _, f in self._class_functions[class_name]):
                raise ValueError
            for m, f in self._class_functions[class_name]:
                self._mapping[(m, url)] = f
        elif any(f not in self._assigned for _, f in self._class_functions[class_name]):
                raise ValueError
        self._class_by_name[class_name] = t

    @staticmethod
    def get_function_class(func: Callable) -> str:
        path = func.__qualname__.split(".")
        if len(path) < 2:
            raise TypeError
        return path[-2]