
from server import items

# STARTING_HP = 20
# STARTING_ACC = 90
# STARTING_MAX_DMG = 6
# STARTING_MIN_DMG = 2
# STARTING_DEF = 10
# STARTING_ARM = 0
# STARTING_SPD = 5

BASE_STATS = {
    'maxHp': 20,
    'accuracy': 90,
    'maxDamage': 6,
    'minDamage': 2,
    'defense': 10,
    'armor': 0,
    'speed': 5
}


class Character:

    def __init__(self, name, starting_stats):
        self.name = name
        self.wounds = 0

        for stat in BASE_STATS:
            if not stat in starting_stats:
                starting_stats[stat] = BASE_STATS[stat]

        self.stats = starting_stats
        self.inventory = items.ItemContainer(name + "-backpack")

    def get_stat(self, stat):
        return self.stats[stat]

    def heal_damage(self, healing):
        if healing < 0: return False

        self.wounds -= healing
        if self.wounds <= 0:
            self.wounds = 0

        return True

    def deal_damage(self, damage):
        total_damage = damage - self.get_stat('armor')
        print("DEBUG: ", self.get_stat('armor'))
        if total_damage < 0: return False
        self.wounds += total_damage
        return True

    def get_hp_left(self):
        return self.get_stat('maxHp') - self.wounds

    def action_used(self, actor, current_room):
        return []

    def display_stats(self):
        msg = self.name + ':\n\t'
        msg += "HP: " + str(self.get_stat("maxHp") - self.wounds) + ' / ' + str(self.get_stat("maxHp"))
        msg += '\n\t'
        for stat in self.stats:
            msg += stat + ': '
            msg += str(self.stats[stat])
            msg += '\n\t'
        return msg


class Player(Character):

    def __init__(self, number, name, uuid, **starting_stats):
        super(Player, self).__init__(name, starting_stats)

        self.number = number
        self.uuid = uuid

        self.weapon = None
        self.armor_equiped = None
        self.accessory = None

    def __repr__(self):
        return self.name + "(player " + str(self.number) + ")"

    def receive_item(self, item):
        self.inventory.add_item(item)

    def get_stat(self, stat):
        value = self.stats[stat]
        if self.weapon is not None:
            value += self.weapon.get_stat(stat)
        if self.armor_equiped is not None:
            value += self.armor_equiped.get_stat(stat)
        if self.accessory is not None:
            value += self.accessory.get_stat(stat)
        return value

    def describe(self):
        return "it's " + self.name


class Monster(Character):

    def __init__(self, name, **starting_stats):
        super(Monster, self).__init__(name, starting_stats)

    def describe(self):
        return self.display_stats()

    def action_used(self, actor, current_room):
        print("TODO do something to the actor")
        return [{
            "message": "a scary monster is after you!",
            "dest": {
                "type": "uuid",
                "value": actor.uuid
            }
        }]

