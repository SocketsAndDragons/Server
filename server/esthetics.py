

class Esthetic:

    def __init__(self, name, description=None, article=''):
        self.name = name
        self.prefix = 'There is ' + article
        if description is None:
            self.description = name
        else:
            self.description = description

    def describe(self):
        return self.description

    def action_used(self, actor, current_room):
        return []

    def on_enter(self, player):
        return [{
            "message": self.description,
            "dest": {
                "type": "uuid",
                "value": player.uuid
            }
        }]