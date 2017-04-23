from Server.sagServer import room

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