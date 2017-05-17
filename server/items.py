

BASE_STATS = {
    'maxHp': 0,
    'accuracy': 0,
    'maxDamage': 0,
    'minDamage': 0,
    'defense': 0,
    'armor': 0,
    'speed': 0
}


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

    def get_stat(self, stat):
        return self.stats[stat]


class ItemContainer:

    def __init__(self, name, *starting_items):
        self.name = name
        self.items = list(starting_items)

    def receive_item(self, item):
        self.add_item(item)

    def size(self):
        return len(self.items)

    def describe(self):
        msg = self.name
        for item in self.items:
            msg += "\n\t" + item.name
        return msg

    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item

    def remove_item(self, item):
        self.items.remove(item)

    def remove_item_name(self, name):
        for i in range(len(self.items)):
            item = self.items[i]
            if item.name == name:
                self.items.remove(item)
                return True
        return False

    def clear(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def __contains__(self, name):
        for item in self.items:
            if item.name == name:
                return True
        return False


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
        player.heal_damage(10)
        woundsHealed = initWounds-player.wounds
        return "you healed " + str(woundsHealed)


class PoisonPotion(Item):

    def __init__(self, name="poison potion"):
        super(PoisonPotion, self).__init__(name, True, "deals 10 damage")

    def use(self, player):
        initWounds = player.wounds
        player.deal_damage(10)
        damage_dealt = player.wounds-initWounds
        return "you suffered " + str(damage_dealt) + " damage"

