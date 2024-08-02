import unittest

from src.container import IoCContainer


class ContainerTest(unittest.TestCase):

    def test_sorting(self): ...

    def test_components(self):
        class Repository: ...

        class Service:

            def __init__(self, repository: Repository):
                self.repository = repository

        class Controller:

            def __init__(self, service: Service):
                self.service = service

        container = IoCContainer()
        container.register_component(Repository)
        container.register_component(Service)
        container.register_component(Controller)

        components = container.start()

        self.assertIsInstance(components[Repository], Repository)
        self.assertIsInstance(components[Service], Service)
        self.assertIsInstance(components[Controller], Controller)