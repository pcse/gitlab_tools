import unittest
import sys

from src import hello_world

class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.__delta = 0.00000001

    def test_say_hello_exact(self):
        self.assertEqual("Hello World!", hello_world.say_hello(),
                        msg='The say_hello() method is not an exact match for \"Hello World!\"')

    def test_say_hello_words(self):
        self.assertTrue("hello world" in hello_world.say_hello().lower(),
                     msg='The say_hello() method does not contain right words')

    def test_say_hello(self):
        self.assertTrue("hello" in hello_world.say_hello().lower(),
                        msg='The say_hello() method does not contain \"Hello\" with any capitalization')

    def test_say_hello_capitalized(self):
        self.assertTrue("Hello" in hello_world.say_hello(),
                        msg='The say_hello() method does not contain \"Hello\"')

    def test_say_world(self):
        self.assertTrue("world" in hello_world.say_hello().lower(),
                        msg='The say_hello() method does not contain \"World\" with any capitalization')

    def test_say_world_capitalized(self):
        self.assertTrue("World" in hello_world.say_hello(),
                        msg='The say_hello() method does not contain \"World\"')

    def test_say_hello_world_with_feeling(self):
        self.assertTrue("!" in hello_world.say_hello(),
                        msg='The say_hello() method does not contain \"!\"')


if __name__ == '__main__':
    unittest.main()
