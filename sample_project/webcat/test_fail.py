"""
Failure based on improper exam configuration
"""

import unittest
from exam import exam

class TestFail(unittest.TestCase):

    def test_fail(self):
        self.fail("Invalid section {} or exam {} ! ", exam.section(), exam.exam())

if __name__ == '__main__':
    unittest.main()
