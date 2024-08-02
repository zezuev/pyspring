import inspect
from typing import Any


type Dependency = tuple[str, type]


class IoCContainer:

    def __init__(self):
        self._dependencies: dict[type, set[Dependency]] = {}
        self._components: dict[type, Any] = {}
        self._class_by_name: dict[str, type] = {}

    def start(self) -> dict[type, Any]:
        dependencies = {
            k: {t for _, t in self._dependencies[k]}
            for k in self._dependencies
        }
        sorting = self.get_topological_sorting(dependencies)
        return {t: self.get_component(t) for t in sorting}

    def get_component[T](self, t: type[T] | str) -> T:
        if isinstance(t, str):
            t = self._class_by_name[t]

        if component := self._components.get(t):
            return component

        inject = {
            name: self.get_component(dependency)
            for name, dependency in self._dependencies[t]
        }
        component = t(**inject)
        self._components[t] = component
        return component

    def register_component[T](self, t: type[T]):
        dependencies = inspect.get_annotations(t.__init__)
        self._dependencies[t] = set(dependencies.items())
        self._class_by_name[t.__name__] = t

    @staticmethod
    def get_topological_sorting[T](dependencies: dict[T, set[T]]):
        sorting: list[T] = []

        def dfs(x: T):
            if x in sorting:
                return
            for d in dependencies.get(x, set()):
                dfs(d)
            sorting.append(x)

        for x in dependencies:
            dfs(x)
        return sorting