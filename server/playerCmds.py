from server import room
from shell import shell
from server import player
import dungeon_server

def encode_direction(direction):
    dir = direction.lower()
    if dir == "north" or dir == 'n':
        return room.NORTH
    elif dir == 'east' or dir == 'e':
        return room.EAST
    elif dir == 'south' or dir == 's':
        return room.SOUTH
    elif dir == 'west' or dir == 'w':
        return room.WEST
    else:
        raise Exception("playerCmds.MoveCommand.encode_direction TODO make an error msg")


class MoveCommand:

    def __init__(self, map):
        self.map = map
        self.short_help_msg = "Move to the room in the indicated direction."

    def help(self):
        shell.Shell().display(self.short_help_msg)

    def execute(self, args, src):
        direction = args[1]
        x, y = self.map.findPlayerByUuid(src)

        print("old_room -- (x:", x, 'y:', y, ')')
        old_room = self.map.rooms[y][x]
        dir_code = encode_direction(direction)

        if not room.direction_is_cardinal(dir_code):
            return self.get_fail_events("you can only move in a cardinal direction (north, south, east or west)")
        if not old_room.has_doors(dir_code):
            return self.get_fail_events("there is no door in that direction!")

        old_addr = (x, y)
        x, y = self.get_new_room_addr(x, y, dir_code)
        new_room = self.map.rooms[y][x]
        success = self.do_move(old_room, new_room, src)

        return self.get_events(src, direction, old_addr, (x,y))

    def get_events(self, uuid, move_direction, room_entered, room_exited):
        player_name = dungeon_server.Server().players[uuid].name

        return [{
            "src": player_name,
            "name": "move",
            "dest": {"type": "room", "x": room_entered[0], "y": room_entered[1]},
            "message": player_name + " left the room to the " + move_direction + "."
        },
        {
            "src": player_name,
            "name": "move",
            "dest": {"type": "room", "exclude": [uuid], "x": room_exited[0], "y": room_exited[1]},
            "message": "player " + player_name + " entered the room."
        },
        {
            "src": player_name,
            "name": "move",
            "dest": {"type": "uuid", "value": uuid},
            "success": True,
            "message": "you moved to the " + move_direction
        }]

    def get_new_room_addr(self, x, y, direction):
        if direction == room.NORTH:
            y -= 1
        elif direction == room.EAST:
            x += 1
        elif direction == room.SOUTH:
            y += 1
        elif direction == room.WEST:
            x -= 1
        print('new_room -- (x:', x, 'y:', y, ')')
        return (x, y)

    def do_move(self, old_room, new_room, uuid):
        player = None
        # try:
        player = dungeon_server.Server().players[uuid]
        new_room.entities.append(player)
        old_room.entities.remove(player)

        return True

    def get_fail_events(self, msg, uuid):
        return [{
            "name": "move",
            "success": False,
            "message": msg,
            "dest": {"type": "uuid", "value": uuid},
        }]


class PingCommand:

    def __init__(self, map):
        self.map = map
        self.short_help_msg = "is the server alive?"

    def help(self):
        shell.Shell().display(self.short_help_msg)

    def execute(self, args, src):
        player_name = src
        message = "Pong!"
        return [{
            "name": "pong",
            "message": "Pong!",
            "dest": {
                "type": "uuid",
                "value": src
            }
        }]

class SayCommand:

    def __init__(self, map):
        self.map = map
        self.short_help_msg = "say something to other players in the same room. This does not cost an action."

    def help(self):
        shell.Shell().display(self.short_help_msg)

    def execute(self, args, src):
        player_name = dungeon_server.Server().players[src].name
        message = player_name + " says \"" + self.get_message(args) + "\""

        current_room = 'd2'
        x = 3
        y = 1
        return [{
            "src": player_name,
            "name": "say",
            "dest": {"type": "room", "x": x, "y": y},
            "message": message,
        }]

    def get_message(self, args):
        return " ".join(args[1:])


class ShoutCommand:

    def __init__(self, map):
        self.map = map
        self.short_help_msg = "say something to other players in the same room. This does not cost an action."

    def help(self):
        shell.Shell().display(self.short_help_msg)

    def execute(self, args, src):
        player_name = dungeon_server.Server().players[src].name
        message = player_name + " shouted \"" + self.get_message(args) + "\""

        return [{
            "src": player_name,
            "name": "say",
            "dest": {"type": "all"},
            "message": message,
        }]

    def get_message(self, args):
        return " ".join(args[1:])


class WhisperCommand:

    def __init__(self, map):
        self.map = map
        self.short_help_msg = "say something to other players in the same room. This does not cost an action."

    def help(self):
        shell.Shell().display(self.short_help_msg)

    def execute(self, args, src):
        player_name = dungeon_server.Server().players[src].name
        if len(args) < 4 or args[1] != 'to':
            return dungeon_server.Server().send_error_event("malformed whisper command, try 'whisper to <name> <message>...", src)
        whisper_target = args[3]

        server = dungeon_server.Server()
        x, y = server.map.findPlayerByUuid(src)
        current_room = server.map.get_room(x, y)

        target = None
        for entity in current_room.entities:
            if entity.name == whisper_target and type(entity) == player.Player:
                target = entity.uuid
                break
        if target is None:
            return dungeon_server.Server().send_error_event(player_name + " is not in this room.", src)

        message = player_name + " whispered to you \"" + self.get_message(args) + "\""
        return [{
            "src": player_name,
            "name": "say",
            "dest": {"type": "uuid", "value": target},
            "message": message,
        }]

    def get_message(self, args):
        return " ".join(args[1:])



