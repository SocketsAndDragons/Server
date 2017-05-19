from server import characters
import dungeon_server
from server.characters import Death
class NukeCommand:
	def __init__(self):
		self.short_help_msg = "nuculur bomb"

	def execute(self, args, src):
		server = dungeon_server.Server()
		nuker = server.players[src]
		events = []
		for entity in dungeon_server.Server().players.values():
			death = Death(entity, attacker=nuker)
			events += death.handle_death()
		return events

class MapCommand:

    def __init__(self, map, map_rules=None):
        self.map = map
        self.short_help_msg = "Shows the map."
        if map_rules is not None:
            self.map_rules = map_rules
        else:
            self.map_rules = []
            self.map_rules.append(NumberOfPlayersRule(map))

    def execute(self, args, src):
        msg = self.build_map()
        parser = MapStringParser(msg)
        for rule in self.map_rules:
            parser.parse_with_rule(rule)

        msg = parser.get_map_str()
        return [{
            "message": msg,
            "width": self.map.width(),
            "height": self.map.height(),
            "dest": {
                "type": "uuid",
                "value": src
            }
        }]

    def build_map(self):
        msg, num_cols = self.get_map_header()
        msg += '\n'
        number_of_rows = len(self.map.rooms)
        number_of_cols = len(self.map.rooms[0])
        for row_num in range(number_of_rows):
            row_str = self.get_map_row(row_num, number_of_cols)
            msg += row_str

        return msg

    def get_map_row(self, row_number, num_cols):
        msg = ('     |'*num_cols) + '\n'
        if row_number < 10:
            center = str(row_number+1) + ' |' + msg

        num_dashes = (num_cols*6)
        return '  |' + msg + center + '  |' + msg + '--|' + ('-' * num_dashes) + '\n'


    def get_map_header(self):
        msg = '  |'
        letter = ord('A')
        for i in range(len(self.map.rooms[0])):
            msg += '  ' + chr(letter) + '  |'
            letter += 1

        num_cols = i+1
        num_dashes = (num_cols *6)-1

        msg += '\n--|' + (num_dashes*'-') + '|'

        return msg, num_cols


class SampleMapRule:

    def apply_rule(self, map_str, map):
        lines = map_str.split('\n')

        num_rooms = int((len(lines[0])-3)/6)
        new_lines = [lines[0], lines[1]]
        for i in range(2, len(lines)-4, 4):
            line = lines[i+1]
            offset = 3
            for j in range(num_rooms):
                index = offset + (j*6)+2
                letter = chr(j+65)
                line = line[:index-1] + letter + str(int(i/4)+1) + line[index+1:]
            new_lines.append(lines[i])
            new_lines.append(line)
            new_lines.append(lines[i+2])
            new_lines.append(lines[i+3])

        return "\n".join(new_lines)


class MapStringParser:

    def __init__(self, map_str):
        self.map_str = map_str
        self.lines = map_str.split('\n')
        self.n_rooms = int((len(self.lines[0])-3)/6)
        self.n_cols = int((len(self.lines[0])-3)/6)

    def parse_with_rule(self, rule):
        new_lines = []
        new_lines.append(rule.header_info(self.lines[0], self.n_rooms))
        new_lines.append(rule.header_border(self.lines[1], self.n_rooms))
        for i in range(5, len(self.lines), 4):
            index = int((i-5)/4)
            new_lines[i-4] = rule.room_top_border(self.lines[i-4], index, self.n_rooms)
            new_lines.append(rule.room_top(self.lines[i-3], index, self.n_rooms))
            new_lines.append(rule.room_middle(self.lines[i-2], index, self.n_rooms))
            new_lines.append(rule.room_bottom(self.lines[i-1], index, self.n_rooms))
            new_lines.append(rule.room_bottom_border(self.lines[i], index, self.n_rooms))
        self.lines = new_lines

    def get_map_str(self):
        return "\n".join(self.lines)

    def __repr__(self):
        return self.get_map_str()

    def __str__(self):
        return self.get_map_str()


class ParserRuleTemplate:

    def header_info(self, line, n_rooms):
        return line

    def header_border(self, line, n_rooms):
        return line

    def room_top_border(self, line, index, n_rooms):
        return line

    def room_top(self, line, index, n_rooms):
        return line

    def room_bottom(self, line, index, n_rooms):
        return line

    def room_bottom_border(self, line, index, n_rooms):
        return line


class RoomNumberRule(ParserRuleTemplate):

    def room_middle(self, line, index, n_rooms):
        offset = 3
        for j in range(n_rooms):
            split_index = offset + (j * 6) + 2
            letter = chr(j+65)
            line = line[:split_index - 1] + letter + str(int(index / 4) + 1) + line[split_index + 1:]

        return line


class NumberOfPlayersRule(ParserRuleTemplate):

    def __init__(self, map):
        self.map = map

    def room_middle(self, line, index, n_rooms):
        offset = 3
        ls = []
        for j in range(n_rooms):
            room = self.map.rooms[index][j]
            split_index = offset + (j * 6) + 2
            num_players = 0
            ls += room.entities
            for entity in room.entities:
                # if type(entity) == characters.Player:
                num_players += 1
            line = line[:split_index] + str(num_players) + line[split_index + 1:]

        return line


class MockMap:

    def __init__(self):
        self.rooms = []
        self.rooms.append(["roomA1", "roomB1", "roomC1"])
        self.rooms.append(["roomA2", "roomB2", "roomC2"])
        self.rooms.append(["roomA3", "roomB3", "roomC3"])

if __name__ == "__main__":
    map = MockMap()
    cmd = MapCommand(map, [RoomNumberRule()])
    print("\nevents:\n", cmd.execute([], "src"))
