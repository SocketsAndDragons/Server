#!/usr/bin/python3

import dungeon_server
import destination

from server import gmCmds
from server import playerCmds
from server import combatCmds
from server import items
from server import characters
from server import esthetics


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
server.cmds["disconnect"] = playerCmds.DisconnectCommand()

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

spooky_crypt = "This room is filled with spooky stone sarcophagi. Hopefully, everything inside is still dead..."
rooms[0][3].entities = [esthetics.Esthetic("spooky crypt", spooky_crypt)]

menacing_drip = """Somewhere in the darkness, a drop of water smacks the cold stone floor.
Another drop falls, hidden somewhere in the dark.
Who knows what else lurks out there with the menacing drip drip in the dark."""
rooms[2][3].entities = [esthetics.Esthetic("menacing drip", menacing_drip)]

shattered_statue = "A shattered ancient statue stands in the middle of the room, alone, except for the dark."
rooms[1][4].entities = [esthetics.Esthetic("shattered statue", shattered_statue)]

bottomless_pit = "There is a pit in the middle of the room with no perceivable bottom."
bottomless_pit += "Its darkenss swollows anything bright that comes near."
rooms[1][2].entities = [esthetics.Esthetic("bottomless pit", bottomless_pit)]

old_smoke = "old expired torch smoke clings thickly in the air here."
rooms[0][1].entities = [esthetics.Esthetic("old smoke", old_smoke)]

server.start_socket()
server.run()

print("exit")
