
NONE = 0b0000
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000
ALL_DOORS = 0b1111


def direction_is_cardinal(direction):
    if direction == 0:
        return False
    return direction == (direction & -direction)


def decode_direction(direction, verbose=False):
    msg = ''
    if (direction & NORTH) != 0:
        msg += 'n'
    if (direction & EAST) != 0:
        msg += 'e'
    if (direction & SOUTH) != 0:
        msg += 's'
    if (direction & WEST) != 0:
        msg += 'w'

    if verbose:
        return verboseify_direction_string(msg)
    return msg


def verboseify_direction_string(dirStr):
    if 'n' in dirStr and 's' in dirStr:
        raise Exception("TODO define an exception type: cannot verboseify 'north south'")
    if 'e' in dirStr and 'w' in dirStr:
        raise Exception("TODO define an exception type: cannot verboseify 'east west'")

    msg = ''

    if 'n' in dirStr:
        msg += 'north '
    elif 'e' in dirStr:
        msg += 'south '
    if 'e' in dirStr:
        msg += 'east '
    elif 'w' in dirStr:
        msg += 'west '

    return msg.strip()


def encode_direction(direction):
    dir = expand_direction_string(direction)
    code = 0
    if "north" in dir:
        code |= NORTH
    if 'east' in dir:
        code |= EAST
    if 'south' in dir:
        code |= SOUTH
    if 'west' in dir:
        code |= WEST
    if 'all' in dir:
        code |= ALL_DOORS

    return code


def expand_direction_string(direction):
    dir = direction.lower()

    forbidden_letters = ['b','c','d','f','g','i','j','k','l','m','p','q','v','x','y','z']
    for letter in forbidden_letters:
        if letter in dir:
            raise Exception("illegal letter in direction code! \n\tTODO define/chose exception type")

    if ("north" in dir) or ("east" in dir) or ("south" in dir) or ("west" in dir):
        return dir

    code = ''
    if "n" in direction:
        code += 'north '
    if "e" in direction:
        code += 'east '
    if "s" in direction:
        code += 'south '
    if "w" in direction:
        code += 'west '

    return code.strip()


class Room:

    def __init__(self, doors=ALL_DOORS, entities=None):
        self.doors = doors

        if not entities is None:
            self.entities = entities
        else:
            self.entities = []

    def has_doors(self, door_code):
        return bool(self.doors & door_code)

    def has_north_door(self):
        return bool(self.doors & NORTH)

    def has_east_door(self):
        return bool(self.doors & EAST)

    def has_south_door(self):
        return bool(self.doors & SOUTH)

    def has_west_door(self):
        return bool(self.doors & WEST)

    def set_north_door(self, bool):
        self._setDoors_(bool, NORTH)

    def set_east_door(self, bool):
        self._setDoors_(bool, EAST)

    def set_south_door(self, bool):
        self._setDoors_(bool, SOUTH)

    def set_west_door(self, bool):
        self._setDoors_(bool, WEST)

    def _setDoors_(self, bool, door_set):
        if bool:
            self.doors |=  door_set
        else:
            self.doors &= (ALL_DOORS ^ door_set)

    def containsEntity(self, entityName):
        for entity in self.entities:
            print("entities:", self.entities)
            if entity.name == entityName:
                return True
        return False

    def removeEntityByName(self, entityName):
        for i in range(len(self.entities)):
            if self.entities[i].name == entityName:
                del self.entities[i]
                return True
        return False

    def getEntityByName(self, entityName):
        for i in range(len(self.entities)):
            if self.entities[i].name == entityName:
                return self.entities[i]
