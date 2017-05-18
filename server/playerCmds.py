from server import room
from shell import shell
from server import characters
from server import items
from server import dungeon_map
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

class LookCommand:

    def __init__(self, map):
        self.map = map
        self.short_help_msg = "Describes the room you're in."

    def help(self):
        shell.Shell().display(self.short_help_msg)

    def execute(self, args, src):
        player_name = src

        x, y = self.map.findPlayerByUuid(src)

        print("room -- (x:", x, 'y:', y, ')')
        room = self.map.rooms[y][x]

        message = "You look around the room.\n"

        players = []
        for entity in room.entities:
            if isinstance(entity, characters.Player):
                players.append(entity.name)

        if len(players) > 0:
            player_string = ", ".join(players)
            message += "You see " + player_string + "\n"
        else:
            message += "You see no other people."

        if room.has_north_door():
            message += "There is a door to the north\n"
        if room.has_east_door():
            message += "There is a door to the east\n"
        if room.has_south_door():
            message += "There is a door to the south\n"
        if room.has_west_door():
            message += "There is a door to the west\n"

        return [{
            "name": "looking",
            "message": message,
            "dest": {
                "type": "uuid",
                "value": src
            }
        }]

def get_players_room(uuid):
    server = dungeon_server.Server()
    x, y = server.map.findPlayerByUuid(uuid)
    return server.map.get_room(x, y)


class MoveCommand:

    def __init__(self, map):
        self.map = map
        self.short_help_msg = "Move to the room in the indicated direction."

    def help(self):
        print(self.short_help_msg)

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
        print(self.short_help_msg)

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
        print(self.short_help_msg)

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
        print(self.short_help_msg)

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
        print(self.short_help_msg)

    def execute(self, args, src):
        player_name = dungeon_server.Server().players[src].name
        if len(args) < 4 or args[1] != 'to':
            msg = "malformed whisper command, try 'whisper to <name> <message>...'"
            dungeon_server.Server().send_error_event(msg, src)
            return []

        whisper_target = args[2]
        current_room = get_players_room(src)
        # server = dungeon_server.Server()
        # x, y = server.map.findPlayerByUuid(src)
        # current_room = server.map.get_room(x, y)

        target = None
        for entity in current_room.entities:
            if entity.name == whisper_target and type(entity) == characters.Player:
                target = entity.uuid
                break
        if target is None:
            msg = whisper_target + " is not in this room."
            dungeon_server.Server().send_error_event(msg, src)
            return []

        message = whisper_target + " whispered to you \"" + " ".join(args[3:]) + "\""
        return [{
            "src": player_name,
            "name": "say",
            "dest": {"type": "uuid", "value": target},
            "message": message,
        }]


class ExamineEntityCommand:

    def help(self):
        print("shows the type of the entity")

    def execute(self, args, src):
        if len(args) != 2:
            msg = "malformed examine command, try 'examine [thing]'"
            dungeon_server.Server().send_error_event(msg, src)
            return []

        entity_name = args[1]
        current_room = get_players_room(src)
        for entity in current_room.entities:
            if entity.name == entity_name:
                return self.handle_target_entity(entity, src)

        msg = "there is no entity by that name"
        dungeon_server.Server().send_error_event(msg, src)
        return []

    def handle_target_entity(self, entity, src):
        if hasattr(entity, "describe"):
            msg = entity.describe()
        else:
            msg = str(type(entity))

        return [{
            "message": msg,
            "dest": {
                "type": "uuid",
                "value": src
            }
        }]


class InvCommand:

    def help(self):
        print("displays all the items in the player's inventory")

    def execute(self, args, src):
        player = dungeon_server.Server().players[src]
        msg = ''
        for item in player.inventory.items:
            msg += item.name + '\n'

        if msg == '':
            msg = "there are no items in your inventory"

        return [{
            "message": msg,
            "dest": {
                "type": "uuid",
                "value": src
            }
        }]


class TakeFromCommand:

    def __init__(self):
        pass

    def help(self):
        print("take an item from a container and place it in the character's inventory")

    def execute(self, args, src):
        if not "from" in args:
            msg = "malformed take command, try 'take <item> from <container>...'"
            dungeon_server.Server().send_error_event(msg, src)
            return []
        from_index = args.index("from")
        item_name = " ".join(args[1:from_index])
        container_name = " ".join(args[from_index+1:])

        current_room = get_players_room(src)
        for entity in current_room.entities:
            if entity.name != container_name:
                continue
            if type(entity) != items.ItemContainer:
                msg = "entity '" + container_name + "' is not a container"
                dungeon_server.Server().send_error_event(msg, src)
                return []
            item = entity.get_item(item_name)
            if item is None:
                msg = "entity '" + container_name + "' does not contain the item '" + item_name + "'"
                dungeon_server.Server().send_error_event(msg, src)
                return []

            player = dungeon_server.Server().players[src]
            player.inventory.add_item(item)
            print("removal successful:", entity.remove_item(item))
            break

            # self.get_events(container_name, item_name, player)

        x, y = dungeon_server.Server().map.findPlayerByUuid(src)
        return [{
            "message": player.name + " has taken a '" + item_name + "' from the '" + container_name + "'",
            "dest": {
                "type": "room",
                "x": x,
                "y": y,
                "exclude": [player.uuid]
            }
        }, {
            "message": "you took the '" + item_name + "' from the '" + container_name + "'",
            "dest": {
                "type": "uuid",
                "value": player.uuid,
            }
        }]


class GiveToCommand:

    def __init__(self):
        pass

    def help(self):
        print("give an item from your inventory to the designated entity")

    def execute(self, args, src):
        server = dungeon_server.Server()

        if not "to" in args:
            msg = "malformed take command, try 'take <item> from <container>...'"
            server.send_error_event(msg, src)
            return []
        to_index = args.index("to")
        item_name = " ".join(args[1:to_index])
        entity_name = " ".join(args[to_index+1:])

        player = server.players[src]

        item = player.inventory.get_item(item_name)
        if item is None:
            msg = "you do not have a '" + item_name + "' to give"
            server.send_error_event(msg, src)
            return []

        current_room = get_players_room(src)
        for entity in current_room.entities:
            if entity.name == entity_name:
                print()
                print("give entity:\n\t", type(entity))
                break
                # if the entity cannot receive items
        if not hasattr(entity, "receive_item"):
            player.inventory.add_item(item)
            msg = "'" + entity_name +"' cannot receive items"
            server.send_error_event(msg, src)
            return []
        entity.receive_item(item)
        player.inventory.remove_item(item)
        events = []
        new_event = {
            "message": "you gave the '" + item_name + "' to '" + entity_name + "'",
            "dest": {"type": "uuid", "value": src}
        }
        events.append(new_event)
        if type(entity) == characters.Player:
            new_event = {
                "message": player.name + " gave you a '" + item_name + "'",
                "dest": {"type": "uuid", "value": entity.uuid}
            }
            events.append(new_event)

        return events


class UseItemCommand:

    def __init__(self):
        self.short_help_msg = "uses an item from the player's inventory"

    def help(self):
        print(self.short_help_msg)

    def execute(self, args, src):
        server = dungeon_server.Server()
        player = server.players[src]

        item_name = " ".join(args[1:])
        item = player.inventory.get_item(item_name)
        if item is None:
            msg = "you do not have the item '" + item_name + "'"
            server.send_error_event(msg, src)
            return []
        msg = "you used your '" + item_name + "'\n"
        msg += item.use(player)
        if item.singleUse:
            player.inventory.remove_item(item)
            msg += "\nyour '" + item_name + "' was used up"

        x, y = server.map.findPlayerByUuid(src)
        return [{
            "message": msg,
            "dest": {"type": "uuid", "value": src}
        },
        {
            "message": player.name + "used a '" + item_name + "'",
            "dest": {"type": "room", "x": x, "y": y, "exclude": [src]}
        }]


# class LookCommand:
#
#     def help(self):
#         print("lists all entities in the room")
#
#     def execute(self, args, src):
#         player = dungeon_server.Server().players[src]
#         current_room = get_players_room(src)
#         msg = 'room:\n\t'
#         for entity in current_room.entities:
#             if entity.name == player.name:
#                 continue
#             msg += entity.name
#             msg += '\n\t'
#
#         return [{
#             "message": msg,
#             "dest": {"type": "uuid", "value": src}
#         }]


class StatsCommand:

    def __init__(self):
        self.short_help_msg = "uses an item from the player's inventory"

    def help(self):
        print(self.short_help_msg)

    def execute(self, args, src):
        server = dungeon_server.Server()
        player = server.players[src]
        msg = player.name + ':\n\t'
        msg += "HP: " + str(player.get_stat("maxHp") - player.wounds) + ' / ' + str(player.get_stat("maxHp"))
        msg += '\n\t'
        for stat in player.stats:
            msg += stat + ': '
            msg += str(player.stats[stat])
            msg += '\n\t'

        return [{
            "message": msg,
            "dest": {"type": "uuid", "value": src}
        }]
