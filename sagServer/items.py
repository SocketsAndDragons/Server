from Server.sagServer.shell import Shell


class Equipment:

    def __init__(self, type, name, maxHp=0, accuracy=0, maxDamage=0, minDamage=0, defense=0, armor=0, speed=0):
        type = type.lower()
        if type != 'armor' and type != 'weapon' and type != 'accessory':
            raise Exception("equipment was given an invalid type")
        self.type = type
        self.name = name
        self.description = ''

        self.maxHp = maxHp
        self.accuracy = accuracy
        self.maxDamage = maxDamage
        self.minDamage= minDamage
        self.defense = defense
        self.armor = armor
        self.speed = speed

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