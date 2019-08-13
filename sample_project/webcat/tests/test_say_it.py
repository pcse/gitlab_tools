import unittest
import os
import subprocess


class TestSayIt(unittest.TestCase):

    def setUp(self):
        self.__timeout = 2
        self.__path = "src/"  # For testing; change to src for release to students


    def test_if_main(self):

        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"hello_world.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="hello_world.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))

    def test_say_it(self):
        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"say_it.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="say_it.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))

    # Just repeats to balance points
    def test_say_it2(self):
        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"say_it.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="say_it.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))

    # Just repeats to balance points
    def test_say_it3(self):
        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"say_it.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="say_it.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))

    # Just repeats to balance points
    def test_say_it4(self):
        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"say_it.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="say_it.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))

    # Just repeats to balance points
    def test_say_it5(self):
        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"say_it.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="say_it.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))

    # Just repeats to balance points
    def test_say_it6(self):
        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"say_it.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="say_it.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))

    # Just repeats to balance points
    def test_say_it7(self):
        expected = "Hello World!"
        try:
            proc = subprocess.Popen(["python "+self.__path+"say_it.py"], stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate(timeout=self.__timeout)
        except TimeoutError:
            self.fail(msg='python hello_world.py timed out.')

        output_str = output.decode('utf-8').rstrip() # Convert bytes and remove the newline added by print
        self.assertEqual(expected, output_str,msg="say_it.py output is incorrect: Expected({}) Actual ({})".format(expected, output_str))


if __name__ == '__main__':
    unittest.main()
