
class Combat:

    def __init__(self, players, monsters):
        if type(players) == dict:
            self.players = players
        elif type(players) == list:
            self.players = self.__build_dict(players)
        else:
            raise Exception("players must be added as either a list or a dictinary")

        if type(players) == dict:
            self.monsters = monsters
        elif type(players) == list:
            self.monsters = self.__build_dict(monsters)
        else:
            raise Exception("monsters must be added as either a list or a dictinary")

        self.actions = {}
        for player_name in self.players:
            self.actions[player_name] = None
        for monster_name in self.monsters:
            self.actions[monster_name] = None

    def __build_dict(self, ls):
        entity_dict = {}
        for entity in ls:
            entity_dict[entity.name] = entity

        return entity_dict

    def describe(self):
        # msg = "it's a fight between "
        # player_names = []
        # for player in self.players:
        #     player_names.append(player.name)
        #
        # msg += ", ".join(player_names)
        #
        # monster_names = []
        # for monster in self.monsters:
        #     monster_names.append(monster.name)
        #
        # msg += " a " + ", a ".join(monster_names)

        return "it's a fight"

    def execute_round(self):
        for actor in self.actions:
            action = self.actions[actor]


