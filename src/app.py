from typing import Any, Callable

from src.container import IoCContainer
from src.router import Router, HttpMethod, Request


class App:

    def __init__(self):
        self.container = IoCContainer()
        self.router = Router()

    def start(self) -> dict[type, Any]:
        return self.container.start()

    def process(self, request: Request) -> Any:
        t = self.router.get_component_type(request)
        component = self.container.get_component(t)
        return self.router.process(request, component)

    def Component[T](self, t: type[T]) -> type[T]:
        self.container.register_component(t)
        return t

    def RestController[T](self, x: type[T] | str) -> type[T]:
        if isinstance(x, str):
            url = x
            def _RestController(t: type[T]):
                self.container.register_component(t)
                self.router.register_class(t, url)
            return _RestController
        self.container.register_component(x)
        self.router.register_class(x)
        return x

    def get_mapping(self, x: Callable | str) -> Callable:
        if isinstance(x, str):
            url = x
            def _get_mapping(f: Callable) -> Callable:
                self.router.register_function(HttpMethod.GET, f, url)
            return _get_mapping
        self.router.register_function(HttpMethod.GET, x)
        return x

    def post_mapping(self, x: Callable | str) -> Callable:
        if isinstance(x, str):
            url = x
            def _post_mapping(f: Callable) -> Callable:
                self.router.register_function(HttpMethod.POST, f, url)
            return _post_mapping
        self.router.register_function(HttpMethod.POST, x)
        return x

    def update_mapping(self, x: Callable | str) -> Callable:
        if isinstance(x, str):
            url = x
            def _update_mapping(f: Callable) -> Callable:
                self.router.register_function(HttpMethod.UPDATE, f, url)
            return _update_mapping
        self.router.register_function(HttpMethod.UPDATE, x)
        return x

    def patch_mapping(self, x: Callable | str) -> Callable:
        if isinstance(x, str):
            url = x
            def _patch_mapping(f: Callable) -> Callable:
                self.router.register_function(HttpMethod.PATCH, f, url)
            return _patch_mapping
        self.router.register_function(HttpMethod.PATCH, x)
        return x

    def delete_mapping(self, x: Callable | str) -> Callable:
        if isinstance(x, str):
            url = x
            def _delete_mapping(f: Callable) -> Callable:
                self.router.register_function(HttpMethod.DELETE, f, url)
            return _delete_mapping
        self.router.register_function(HttpMethod.DELETE, x)
        return x