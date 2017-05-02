"""
Author: Thomas Bonatti (thomasbonatti2695@gmail.com)
"""

import unittest
from Server.server import map


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

    def testGetRoomAddrSingleDigit(self):
        myMap = map.Map(2, 4)
        x, y = myMap.getRoomAddr('a1')
        assert x == 0
        assert y == 0

    def testGetRoomAddrMultiDigit(self):
        myMap = map.Map(2, 4)
        x, y = myMap.getRoomAddr('d123')
        assert x == 3
        assert y == 122

    def testGetRoom(self):
        myMap = map.Map(3, 4)
        myMap.rooms[1][1] = 10
        self.assertEqual(myMap.getRoom('b2'), 10)

if __name__ == "__main__":
    unittest.main()


