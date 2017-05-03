
import unittest
from Server.server.playerCmds import MoveCommand
from Server.server.playerCmds import SayCommand
from Server.server.map import Map
from Server.server import room


class PlayerMock:
    def __init__(self, name):
        self.name = name


class MoveCommandTest(unittest.TestCase):

    def setUp(self):
        self.map = Map(4, 4)
        self.cmd = MoveCommand(self.map)
        self.player = PlayerMock("player1")
        self.map.rooms[1][1].entities.append(self.player)

    def testMoveRemovesPlayer(self):
        args = ['move', 'player1', 'north']
        self.cmd.execute(args)
        self.assertEqual(len(self.map.rooms[1][1].entities), 0)

    def testMoveAddsPlayerToRoomNorth(self):
        args = ['move', 'player1', 'north']
        self.cmd.execute(args)
        self.assertEqual(len(self.map.rooms[1][0].entities), 1)

    def testMoveAddsPlayerToRoomEast(self):
        args = ['move', 'player1', 'east']
        self.cmd.execute(args)
        self.assertEqual(len(self.map.rooms[2][1].entities), 1)

    def testMoveAddsPlayerToRoomSouth(self):
        args = ['move', 'player1', 'south']
        self.cmd.execute(args)
        self.assertEqual(len(self.map.rooms[1][2].entities), 1)

    def testMoveAddsPlayerToRoomWest(self):
        args = ['move', 'player1', 'west']
        self.cmd.execute(args)
        self.assertEqual(len(self.map.rooms[0][1].entities), 1)

    def testRemoveDoorsThrowsException(self):
        args = ['move', 'player1', 'east']
        self.map.rooms[1][1].doors = room.NORTH | room.WEST
        with self.assertRaises(Exception):
            self.cmd.execute(args)

    def testRemoveDoorsDoesntRemovePlayer(self):
        args = ['move', 'player1', 'west']
        self.map.rooms[1][1].doors = room.NORTH | room.EAST
        try:
            self.cmd.execute(args)
        except:
            pass
        self.assertEqual(len(self.map.rooms[1][1].entities), 1)

    def testRemoveDoorsDoesntMovePlayer(self):
        args = ['move', 'player1', 'west']
        self.map.rooms[1][1].doors = room.NORTH | room.EAST
        try:
            self.cmd.execute(args)
        except:
            pass
            #exception expected
        self.assertEqual(len(self.map.rooms[0][1].entities), 0)


class SayCommandTest(unittest.TestCase):

    def setUp(self):
        self.cmd = SayCommand()

    def testMessage(self):
        args = ['say', 'player1', 'spam', 'and', 'eggs']
        msg = self.cmd.get_message(args)
        self.assertEqual(msg, 'spam and eggs')



if __name__ == "__main__":
    unittest.main()
