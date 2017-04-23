
NONE = 0b0000
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000
ALL_DOORS = 0b1111

class Room:

    def __init__(self, doors=ALL_DOORS, interactions=None):
        if not interactions is None:
            self.interactions = interactions
        else:
            self.interactions = []

        self.doors = doors

    def has_north_door(self):
        return False

    def has_east_door(self):
        return False

    def has_south_door(self):
        return False

    def has_west_door(self):
        return False

    def set_north_door(self, bool):
        pass

    def set_east_door(self, bool):
        pass

    def set_south_door(self, bool):
        pass

    def set_west_door(self, bool):
        pass