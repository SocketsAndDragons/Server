"""
Author: Thomas Bonatti (thomasbonatti2695@gmail.com)
"""

import unittest
from Server.server import room


class EncodeDecodeDirection(unittest.TestCase):

    def testEncodeNorthWestChar(self):
        encoded = room.encode_direction('nw')
        self.assertEqual(encoded, room.NORTH | room.WEST)

    def testEncodeSouthEastWord(self):
        encoded = room.encode_direction('southeast')
        self.assertEqual(encoded, room.SOUTH | room.EAST)

    def testEncodeNorthEastSpace(self):
        encoded = room.encode_direction('north east')
        self.assertEqual(encoded, room.NORTH | room.EAST)

    def testEncodeAll(self):
        encoded = room.encode_direction('north eastsouth west')
        self.assertEqual(encoded, room.ALL_DOORS)

    def testDecodeNorth(self):
        decoded = room.decode_direction(room.NORTH)
        self.assertEqual(decoded, 'n')

    def testDecodeEast(self):
        decoded = room.decode_direction(room.EAST)
        self.assertEqual(decoded, 'e')

    def testDecodeSouth(self):
        decoded = room.decode_direction(room.SOUTH)
        self.assertEqual(decoded, 's')

    def testDecodeWest(self):
        decoded = room.decode_direction(room.WEST)
        self.assertEqual(decoded, 'w')

    def testDecodeNorthVerbose(self):
        decoded = room.decode_direction(room.NORTH, verbose=True)
        self.assertEqual(decoded, 'north')

    def testDecodeNorthWestVerbose(self):
        decoded = room.decode_direction(room.NORTH | room.WEST, verbose=True)
        self.assertEqual(decoded, 'north west')

    def testDecodeSouthEastVerbose(self):
        decoded = room.decode_direction(room.SOUTH | room.EAST, verbose=True)
        self.assertEqual(decoded, 'south east')

    def testDecodeWestEastVerbose(self):
        with self.assertRaises(Exception):
            room.decode_direction(room.WEST | room.EAST, verbose=True)

    def testDecodeNorthSouthVerbose(self):
        with self.assertRaises(Exception):
            room.decode_direction(room.NORTH | room.SOUTH, verbose=True)

    def testDirectionIsCardinalNorth(self):
        assert room.direction_is_cardinal(room.NORTH)

    def testDirectionIsCardinalEast(self):
        assert room.direction_is_cardinal(room.EAST)

    def testDirectionIsCardinalSouth(self):
        assert room.direction_is_cardinal(room.SOUTH)

    def testDirectionIsCardinalWest(self):
        assert room.direction_is_cardinal(room.WEST)

    def testDirectionIsCardinalAll(self):
        assert not room.direction_is_cardinal(room.ALL_DOORS)

    def testDirectionIsCardinalSome(self):
        assert not room.direction_is_cardinal(room.WEST | room.NORTH)

    def testDirectionIsCardinalNone(self):
        assert not room.direction_is_cardinal(room.NONE)


class HasDoorsTest(unittest.TestCase):

    def testHasNorthAllTrue(self):
        myRoom = room.Room(doors=room.ALL_DOORS)
        myRoom.has_doors(room.NORTH)

    def testHasNorthHasNorth(self):
        myRoom = room.Room(doors=room.NORTH)
        myRoom.has_doors(room.NORTH)

    def testHasNorthHasNone(self):
        myRoom = room.Room(doors=room.NONE)
        myRoom.has_doors(room.NORTH)

    def testHasNorthHasWrongDoors(self):
        myRoom = room.Room(doors=(room.SOUTH | room.EAST | room.WEST))
        myRoom.has_doors(room.NORTH)

    def testHasEast(self):
        myDoors = room.EAST
        myRoom = room.Room(doors=myDoors)
        myRoom.has_doors(myDoors)

    def testHasSouth(self):
        myDoors = room.SOUTH
        myRoom = room.Room(doors=myDoors)
        myRoom.has_doors(myDoors)

    def testHasWest(self):
        myDoors = room.WEST
        myRoom = room.Room(doors=myDoors)
        myRoom.has_doors(myDoors)


class FindGetRemoveEntity(unittest.TestCase):

    def setUp(self):
        self.player1 = MockPlayer("player1")
        self.player2 = MockPlayer("player2")
        self.room = room.Room(entities=[self.player1, self.player2])

    def testGetEntityByNameReturnsObject(self):
        assert self.player1 is self.room.getEntityByName('player1')

    def testGetEntityByNameNotThereReturnsNone(self):
        assert self.room.getEntityByName('notThere') is None

    def testRemoveEntityByNameReturnsTrue(self):
        success = self.room.removeEntityByName("player1")
        assert success

    def testRemoveEntityByNameReducesLength(self):
        lenInit = len(self.room.entities)
        self.room.removeEntityByName("player2")
        self.assertEqual(len(self.room.entities), lenInit-1)

    def testRemoveEntityByNameRemovesPlayerOne(self):
        self.room.removeEntityByName("player1")
        for player in self.room.entities:
            if player.name == "player1":
                # should not have this player
                assert False

    def testRemoveEntityByNameNotExistantRemovesNone(self):
        lenInit = len(self.room.entities)
        success = self.room.removeEntityByName("[ajdwpo")
        self.assertEqual(len(self.room.entities), lenInit)

    def testRemoveEntityByNameNotExistantReturnsFalse(self):
        success = self.room.removeEntityByName("not a player")
        assert not success


class TestContainsEntity(unittest.TestCase):

    def setUp(self):
        self.room = room.Room(entities=[MockPlayer("player1"), MockPlayer("player2")])

    def testContainsEntityTrue(self):
        assert self.room.containsEntity("player1")

    def testCotainsPlayerFalse(self):
        assert not self.room.containsEntity("[pkjef[j")

class MockPlayer:

    def __init__(self, name):
        self.name = name

class MapTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDefaultInitEntities(self):
        room1 = room.Room()
        assert room1.entities == []

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