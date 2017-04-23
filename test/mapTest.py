import unittest
from Server.sagServer import map


class MapTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOne(self):
        myMap = map.Map(1, 2)


if __name__ == "__main__":
    unittest.main()


