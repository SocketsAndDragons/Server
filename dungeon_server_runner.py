#!/usr/bin/python3

import dungeon_server
import destination

from server import gmCmds
from server import playerCmds
from server import combatCmds
from server import items
from server import characters


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

server.cmds["attack"] = combatCmds.AttackCommand()

server.dest_rules["uuid"] = destination.UuidDestRule()
server.dest_rules["room"] = destination.RoomDestRule()
server.dest_rules["gm"] = destination.GmDestRule()
server.dest_rules["all"] = destination.AllDestRule()
server.dest_rules["name"] = destination.NameDestRule()

scary_monster_loot = items.ItemContainer("loot", items.HealingPotion())

rooms = server.map.rooms
rooms[1][3].entities = [
        items.ItemContainer("chest", MockItem(), items.HealingPotion(), items.PoisonPotion()),
        characters.Monster("scary monster", maxHp=5, loot=scary_monster_loot)
]

very_scary = characters.Monster("very scary monster", maxHp = 30)
rooms[0][0].entities = [very_scary]

rooms[2][4].entities = [items.ItemContainer("big chest", items.VictoryItem("very shiney coin"))]

server.start_socket()
server.run()

print("exit")
