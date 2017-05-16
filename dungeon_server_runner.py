#!/usr/bin/python3

import dungeon_server
from server import playerCmds
import destination
from server import gmCmds


server = dungeon_server.Server()

server.cmds["say"] = playerCmds.SayCommand(server.map)
server.cmds["shout"] = playerCmds.ShoutCommand(server.map)
server.cmds["look"] = playerCmds.LookCommand(server.map)
server.cmds["whisper"] = playerCmds.WhisperCommand(server.map)
server.cmds["move"] = playerCmds.MoveCommand(server.map)
server.cmds["ping"] = playerCmds.PingCommand(server.map)
server.cmds["map"] = gmCmds.MapCommand(server.map)

server.dest_rules["uuid"] = destination.UuidDestRule()
server.dest_rules["room"] = destination.RoomDestRule()
server.dest_rules["gm"] = destination.GmDestRule()
server.dest_rules["all"] = destination.AllDestRule()
server.dest_rules["name"] = destination.NameDestRule()



server.start_socket()
server.run()

print("exit")
