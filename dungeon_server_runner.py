#!/usr/bin/python3

import dungeon_server
from server import playerCmds
import destination
from server import gmCmds
from server import items

class MockItem:
    def __init__(self):
        self.name = "mock item"


server = dungeon_server.Server()

server.cmds["map"] = gmCmds.MapCommand(server.map)
server.cmds["say"] = playerCmds.SayCommand(server.map)
server.cmds["shout"] = playerCmds.ShoutCommand(server.map)
server.cmds["look"] = playerCmds.LookCommand(server.map)
server.cmds["whisper"] = playerCmds.WhisperCommand(server.map)
server.cmds["move"] = playerCmds.MoveCommand(server.map)
server.cmds["ping"] = playerCmds.PingCommand(server.map)
server.cmds["examine"] = playerCmds.ExamineEntityCommand()
server.cmds["inv"] = playerCmds.InvCommand()
server.cmds["take"] = playerCmds.TakeFromCommand()
server.cmds["give"] = playerCmds.GiveToCommand()
server.cmds["use"] = playerCmds.UseItemCommand()
server.cmds["stats"] = playerCmds.StatsCommand()
server.cmds["help"] = playerCmds.HelpCommand()

server.cmds["nuke"] = gmCmds.NukeCommand()

server.dest_rules["uuid"] = destination.UuidDestRule()
server.dest_rules["room"] = destination.RoomDestRule()
server.dest_rules["gm"] = destination.GmDestRule()
server.dest_rules["all"] = destination.AllDestRule()
server.dest_rules["name"] = destination.NameDestRule()

rooms = server.map.rooms
rooms[1][3].entities = [items.ItemContainer("chest", MockItem(), items.HealingPotion(), items.PoisonPotion())]


server.start_socket()
server.run()

print("exit")
