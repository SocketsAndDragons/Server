

class MapCommand:

    def __init__(self, map, map_rules):
        self.map = map
        self.map_rules = map_rules

    def execute(self, args, src):
        msg = self.build_map()
        for rule in self.map_rules:
            msg = rule.apply_rule(msg, self.map)

        return msg

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


        new_lines = [lines[0], lines[1]]
        for i in range(2, len(lines), 4):
            num_rooms = int((len(line)-3)/6)
            offset = 3
            for i in range(num_rooms):
                index = offset + (i*6)
                line = line[:index] + str(num_rooms) + line[index+1:]
                new_lines.append(line)


        return "\n".join(lines)

    def parse_line(self):
        pass

class MockMap:

    def __init__(self):
        self.rooms = []
        self.rooms.append(["roomA1", "roomB1", "roomC1"])
        self.rooms.append(["roomA2", "roomB2", "roomC2"])
        # self.rooms.append(["roomA3", "roomB3", "roomC3"])

if __name__ == "__main__":
    map = MockMap()
    cmd = MapCommand(map, [SampleMapRule()])
    print(cmd.execute([], "src"))
