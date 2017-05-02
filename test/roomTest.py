"""
Author: Thomas Bonatti (thomasbonatti2695@gmail.com)
"""

import unittest
from Server.sagServer import room


class TestContainsPlayer(unittest.TestCase):

    def setUp(self):
        self.room = room.Room(entities=[MockPlayer("player1"), MockPlayer("player1")])

    def testContainsPlayerTrue(self):
        assert self.room.containsPlayer("player1")

    def testCotainsPlayerFalse(self):
        assert not self.room.containsPlayer("[pkjef[j")

class MockPlayer:

    def __init__(self, name):
        self.name = name

class MapTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDefaultInitPlayers(self):
        room1 = room.Room()
        assert room1.players == []

    def testCustomInitPlayers(self):
        room1 = room.Room(players=10)
        assert room1.players == 10

    def testDefaultInitInteractions(self):
        room1 = room.Room()
        assert room1.interactions == []

    def testCustomInitPlayers(self):
        room1 = room.Room(interactions=10)
        assert room1.interactions == 10

    def testDefaultInitMonsters(self):
        room1 = room.Room()
        assert room1.monsters == []

    def testCustomInitMonsters(self):
        room1 = room.Room(monsters=10)
        assert room1.monsters == 10

    def testDefaultRoomHasAllDoors(self):
        myRoom = room.Room()
        assert myRoom.has_north_door()
        assert myRoom.has_east_door()
        assert myRoom.has_south_door()
        assert myRoom.has_west_door()

    def testRoomHasOnlyNorthDoor(self):
        myRoom = room.Room(room.NORTH)
        assert myRoom.has_north_door()
        assert not myRoom.has_east_door()
        assert not myRoom.has_south_door()
        assert not myRoom.has_west_door()

    def testRoomHasOnlyEastDoor(self):
        myRoom = room.Room(room.EAST)
        assert not myRoom.has_north_door()
        assert myRoom.has_east_door()
        assert not myRoom.has_south_door()
        assert not myRoom.has_west_door()

    def testRoomHasOnlySouthDoor(self):
        myRoom = room.Room(room.SOUTH)
        assert not myRoom.has_north_door()
        assert not myRoom.has_east_door()
        assert myRoom.has_south_door()
        assert not myRoom.has_west_door()

    def testRoomHasOnlyWestDoor(self):
        myRoom = room.Room(room.WEST)
        assert not myRoom.has_north_door()
        assert not myRoom.has_east_door()
        assert not myRoom.has_south_door()
        assert myRoom.has_west_door()

    def testRoomHasTwoDoors(self):
        myRoom = room.Room(room.EAST | room.NORTH)
        print(bin(myRoom.doors))
        assert myRoom.has_north_door()
        assert myRoom.has_east_door()
        assert not myRoom.has_south_door()
        assert not myRoom.has_west_door()

    def testRoomHasNoDoors(self):
        myRoom = room.Room(room.NONE)
        assert not myRoom.has_north_door()
        assert not myRoom.has_east_door()
        assert not myRoom.has_south_door()
        assert not myRoom.has_west_door()

    def testAddNorthDoor(self):
        myRoom = room.Room(room.NONE)
        myRoom.set_north_door(True)
        assert myRoom.has_north_door()

    def testAddEastDoor(self):
        myRoom = room.Room(room.NONE)
        myRoom.set_east_door(True)
        assert myRoom.has_east_door()

    def testAddSouthDoor(self):
        myRoom = room.Room(room.NONE)
        myRoom.set_south_door(True)
        assert myRoom.has_south_door()

    def testAddWestDoor(self):
        myRoom = room.Room(room.NONE)
        myRoom.set_west_door(True)
        assert myRoom.has_west_door()


    def testRemoveNorthDoor(self):
        myRoom = room.Room()
        myRoom.set_north_door(False)
        assert not myRoom.has_north_door()

    def testRemoveEastDoor(self):
        myRoom = room.Room()
        myRoom.set_east_door(False)
        assert not myRoom.has_east_door()

    def testRemoveSouthDoor(self):
        myRoom = room.Room()
        myRoom.set_south_door(False)
        assert not myRoom.has_south_door()

    def testRemoveWestDoor(self):
        myRoom = room.Room()
        myRoom.set_west_door(False)
        assert not myRoom.has_west_door()


if __name__ == "__main__":
    unittest.main()