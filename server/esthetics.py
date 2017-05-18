

class Esthetic:

    def __init__(self, name, description=None):
        self.name = name
        if description is None:
            self.description = name
        else:
            self.description = description

    def describe(self):
        return self.description

    def action_used(self, actor, current_room):
        return []