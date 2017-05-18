from server import room
import dungeon_server

ORD_OFFSET = 97


def getRoomAddr(self, strAddr):
    letter = strAddr[0].lower()
    x = ord(letter) - ORD_OFFSET
    y = int(strAddr[1:])-1
    return x, y


def get_addr_name(self, x, y):
    letter = ord(x + ORD_OFFSET)
    return letter + str(y)


class Map():

    def __init__(self, width, height):
        self.rooms = self.__initRooms__(width, height)
        self.player_spawn = (3, 1)

    def __initRooms__(self, width, height):
        rooms = []
        print("width:", width)
        print("height:", height)
        for i in range(height):
            row = []
            for j in range(width):
                row.append(room.Room())
            rooms.append(row)

        return rooms

    def at_spawn(self, entity):
        if type(entity) == tuple:
            return entity[0] == self.player_spawn[0] and entity[1] == self.player_spawn[1]

        x, y = self.findEntityByName(entity.name)
        return x == self.player_spawn[0] and y == self.player_spawn[1]

    def add_new_player(self, new_player):
        x, y = self.player_spawn
        room = self.get_room(x, y)
        room.entities.append(new_player)

    def height(self):
        return len(self.rooms)

    def width(self):
        return len(self.rooms[0])

    def get_room(self, x, y):
        return self.rooms[y][x]

    def address_of_room(self, room):
        for y in range(len(self.rooms)):
            for x in range(len(self.rooms[y])):
                if self.rooms[y][x] is room:
                    return x, y

    def getRoom(self, strAddr):
        x, y = self.getRoomAddr(strAddr)
        return self.rooms[y][x]

    def findEntityByName(self, playerName):
        for y in range(len(self.rooms)):
            for x in range(len(self.rooms[y])):
                if self.rooms[y][x].containsEntity(playerName):
                    return x, y
        return -1, -1

    def findPlayerByUuid(self, uuid):
        player = dungeon_server.Server().players[uuid]
        name = player.name
        return self.findEntityByName(name)

