"""
Example file for loading unit tests used by WebCAT
This is not generally distributed to students!

We define a comboSuite to combine multiple test files into a single test file
that WebCAT will execute.

"""
import unittest
import sys

from tests import test_hello_world

from tests import test_say_it
from exam import exam

suiteList=[]

if exam.section() == 8529 and exam.exam() == 'A':
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(test_hello_world.TestHelloWorld))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(test_say_it.TestSayIt))
else:
    #print("Invalid section {} or exam {} ! ", exam.section(), exam.exam())
    import test_fail
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(test_fail.TestFail))

# ----------------   Join them together and run them
comboSuite = unittest.TestSuite(suiteList)
unittest.TextTestRunner(verbosity=0).run(comboSuite)
