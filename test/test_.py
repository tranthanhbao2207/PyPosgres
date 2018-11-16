import unittest
import requests

class FirstTest(unittest.TestCase):
    def test_add(self):
        a = 10 + 5
        print(a)
        self.assertEquals(15, a)


if __name__ == "__main__":
    unittest.main()