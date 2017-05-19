
import dungeon_server


class AttackCommand:

    def __init__(self):
        self.action_cost = 1

    def help(self):
        return "attack another entity"

    def execute(self, args, src):
        server = dungeon_server.Server()
        attacker = server.players[src]
        entity_name = " ".join(args[1:])
        if entity_name == attacker.name:
            return [{
                "message": "you cannot attack yourself!",
                "dest": {
                    "type": "uuid",
                    "value": src
                }
            }]

        x, y = server.map.findPlayerByUuid(src)
        current_room = server.map.get_room(x, y)
        for entity in current_room.entities:
            if entity.name != entity_name:
                continue
            result = attacker.attack(entity)
            events = attacker.default_attack_events(entity, result)
            return events

        return [{
            "message": entity_name + " is not in the room with you.",
            "dest": {
                "type": "uuid",
                "value": src
            }
        }]
