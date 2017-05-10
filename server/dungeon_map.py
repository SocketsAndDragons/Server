from server import room

ORD_OFFSET = 97

class Map():

    def __init__(self, width, height):
        self.rooms = self.__initRooms__(width, height)

    def __initRooms__(self, width, height):
        rooms = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(room.Room())
            rooms.append(row)

        return rooms

    def getRoomAddr(self, strAddr):
        letter = strAddr[0].lower()
        x = ord(letter) - ORD_OFFSET
        y = int(strAddr[1:])-1
        return x, y

    def address_of_room(self, room):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                if self.rooms[i][j] is room:
                    return i, j

    def getRoom(self, strAddr):
        x, y = self.getRoomAddr(strAddr)
        return self.rooms[x][y]

    def findEntityByName(self, playerName):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                if self.rooms[i][j].containsEntity(playerName):
                    return i, j
        return -1, -1
