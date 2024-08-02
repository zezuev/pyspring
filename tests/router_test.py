import unittest

from src.router import Router, HttpMethod


class RouterTest(unittest.TestCase):

    def test_process(self):
        class Controller:
            def say_hello(self) -> str:
                return "Hello, World!"

        router = Router()
        router.register_function(HttpMethod.GET, Controller.say_hello, "/api/hello")
        router.register_class(Controller)

        self.assertEqual(
            router.process((HttpMethod.GET, "/api/hello"), Controller()),
            "Hello, World!",
        )