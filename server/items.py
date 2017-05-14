from shell import Shell
from server import stats


BASE_STATS = {
    'maxHp': 0,
    'accuracy': 0,
    'maxDamage': 0,
    'minDamage': 0,
    'defense': 0,
    'armor': 0,
    'speed': 0
}

class Character:

    def __init__(self, name, starting_stats):
        self.name = name
        self.wounds = 0


    def get_stat(self, stat):
        return self.stats[stat]

class Equipment:

    def __init__(self, type, name, **starting_stats): #, maxHp=0, accuracy=0, maxDamage=0, minDamage=0, defense=0, armor=0, speed=0):
        type = type.lower()
        if type != 'armor' and type != 'weapon' and type != 'accessory':
            raise Exception("equipment was given an invalid type")
        self.type = type
        self.name = name
        self.description = ''

        # self.maxHp = maxHp
        # self.accuracy = accuracy
        # self.maxDamage = maxDamage
        # self.minDamage= minDamage
        # self.defense = defense
        # self.armor = armor
        # self.speed = speed

        for stat in BASE_STATS:
            if not stat in starting_stats:
                starting_stats[stat] = BASE_STATS[stat]

        self.stats = starting_stats

class Item:

    def __init__(self, name, singleUse=False, description=''):

        self.name = name
        self.singleUse = singleUse
        self.description = description

    def use(self, player):
        print(player.name, "used a", self.name)
        print("but nothing happend...")


class HealingPotion(Item):

    def __init__(self, name="healing potion"):
        super(HealingPotion, self).__init__(name, True, "heals 10 hp")

    def use(self, player):
        initWounds = player.wounds
        player.healDamage(10)
        woundsHealed = initWounds-player.wounds
        Shell().display(player, "used a healing potion to heal", woundsHealed)
