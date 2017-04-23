import unittest
from Server.sagServer import map


class MapTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInitRoomsWidth(self):
        myMap = map.Map(5, 1)
        myMap.rooms[4][0]
        # as long as an exception isn't thrown, you're good

    def testInitRoomsWidthNotTooBig(self):
        myMap = map.Map(4, 2)
        with self.assertRaises(IndexError):
            myMap.rooms[4][0]
        # as long as an exception isn't thrown, you're good

    def testInitRoomsHeight(self):
        myMap = map.Map(3, 6)
        myMap.rooms[0][5]
        # as long as an exception isn't thrown, you're good

    def testInitRoomsHeightNotToBig(self):
        myMap = map.Map(2, 4)
        with self.assertRaises(IndexError):
            myMap.rooms[0][4]
        # as long as an exception isn't thrown, you're good


if __name__ == "__main__":
    unittest.main()


