"""
Author: Thomas Bonatti (thomasbonatti2695@gmail.com)
"""

import unittest
from server import dungeonMap


class TestMapParsing(unittest.TestCase):

    def setUp(self):
        self.map = dungeonMap.Map(3, 3)
        self.map.rooms[1][0].entities.append(MochPlayer("player1"))
        self.map.rooms[0][2].entities.append(MochPlayer("player2"))

    def testAddressOfRoom(self):
        x = 1
        y = 2
        room = self.map.rooms[x][y]
        result_x, result_y = self.map.address_of_room(room)
        self.assertEqual(result_x, x)
        self.assertEqual(result_y, y)

    def testFindPlayerOne(self):
        x, y = self.map.findEntityByName("player1")
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)

    def testFindNoPlayer(self):
        x, y = self.map.findEntityByName("odysseus")
        self.assertEqual(x, -1)
        self.assertEqual(y, -1)


class MochPlayer:

    def __init__(self, name):
        self.name = name


class MapTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInitRoomsWidth(self):
        myMap = dungeonMap.Map(5, 1)
        myMap.rooms[4][0]
        # as long as an exception isn't thrown, you're good

    def testInitRoomsWidthNotTooBig(self):
        myMap = dungeonMap.Map(4, 2)
        with self.assertRaises(IndexError):
            myMap.rooms[4][0]
        # as long as an exception isn't thrown, you're good

    def testInitRoomsHeight(self):
        myMap = dungeonMap.Map(3, 6)
        myMap.rooms[0][5]
        # as long as an exception isn't thrown, you're good

    def testInitRoomsHeightNotToBig(self):
        myMap = dungeonMap.Map(2, 4)
        with self.assertRaises(IndexError):
            myMap.rooms[0][4]
        # as long as an exception isn't thrown, you're good

    def testGetRoomAddrSingleDigit(self):
        myMap = dungeonMap.Map(2, 4)
        x, y = myMap.getRoomAddr('a1')
        assert x == 0
        assert y == 0

    def testGetRoomAddrMultiDigit(self):
        myMap = dungeonMap.Map(2, 4)
        x, y = myMap.getRoomAddr('d123')
        assert x == 3
        assert y == 122

    def testGetRoom(self):
        myMap = dungeonMap.Map(3, 4)
        myMap.rooms[1][1] = 10
        self.assertEqual(myMap.getRoom('b2'), 10)

if __name__ == "__main__":
    unittest.main()


