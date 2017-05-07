from Server.server import room

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

    def execute(self, args):
        playerName = args[1]
        direction = args[2]
        x, y = self.map.findEntityByName(playerName)
        old_room = self.map.rooms[x][y]
        dir_code = encode_direction(direction)

        if not room.direction_is_cardinal(dir_code):
            self.send_fail_events()
            raise Exception("trying to move in non-cardinal direction\n\tTODO define/select exception type!")
        if not old_room.has_doors(dir_code):
            self.send_fail_events()
            raise Exception("trying to move through non-existent door\n\tTODO define/select exception type!")

        new_room = self.get_new_room(x, y, dir_code)
        success = self.do_move(old_room, new_room, playerName)
        self.send_success_events()

    def get_new_room(self, x, y, direction):
        if direction == room.NORTH:
            y -= 1
        elif direction == room.EAST:
            x += 1
        elif direction == room.SOUTH:
            y += 1
        elif direction == room.WEST:
            x -= 1
        return self.map.rooms[x][y]

    def do_move(self, old_room, new_room, player_name):
        player = old_room.getEntityByName(player_name)
        new_room.entities.append(player)
        old_room.entities.remove(player)
        return True

    def send_success_events(self):
        pass
        #todo send events

    def send_fail_events(self):
        pass
        #todo send events

    def get_events(self, args):
        return [{}]


class SayCommand:

    def execute(self, args):
        playerName = args[1]
        message = args[1] + " says: \"" + self.get_message(args) + "\""

    def get_message(self, args):
        return " ".join(args[2:])

    def get_events(self, args):
        return [{}]


class ShoutCommand:

    def execute(self, args):
        playerName = args[1]
        message = args[1] + " is shouting: \"" + self.get_message(args) + "\""

    def get_message(self, args):
        return " ".join(args[2:])


class WhisperCommand:

    def execute(self, args):
        playerName = args[1]
        message = args[1] + " whispered to you: \"" + self.get_message(args) + "\""

    def get_message(self, args):
        return " ".join(args[2:])

    def get_events(self, args):
        return [{}]


