from typing import Any

from src.container import IoCContainer
from src.router import Router


class App:

    def __init__(self):
        self.container = IoCContainer()
        self.router = Router()

    def Component[T](self, t: type[T]) -> type[T]:
        self.container.register_component(t)
        return t

    def start(self) -> dict[type, Any]:
        return self.container.start()