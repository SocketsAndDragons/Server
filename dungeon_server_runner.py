from Server import dungeon_server
from Server.server import playerCmds


server = dungeon_server.Server()
server.cmds["say"] = playerCmds.SayCommand(server.map)
server.cmds["shout"] = playerCmds.ShoutCommand(server.map)
server.cmds["move"] = playerCmds.MoveCommand(server.map)

server.start_socket()
server.run()

print("exit")