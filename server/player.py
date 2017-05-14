
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

    def get_stat(self, stat):
        return self.stats[stat]


class Player(Character):

    def __init__(self, number, name, uuid, **starting_stats):
        super(Player, self).__init__(name, starting_stats)

        self.number = number
        self.uuid = uuid

        self.weapon = None
        self.armorEquiped = None
        self.accessory = None

    def __repr__(self):
        return self.name + "(player " + str(self.number) + ")"

    def healDamage(self, healing):
        if healing < 0: return False

        self.wounds -= healing
        if self.wounds <= 0:
            self.wounds = 0

        return True

    def dealDamage(self, damage):
        total_damage = damage-self.getArmorStat()
        print("DEBUG: ", self.getArmorStat())
        if total_damage < 0: return False
        self.wounds += total_damage
        return True

    def getHpLeft(self):
        return self.getMaxHp() - self.wounds

    def getMaxHp(self):
        return self.get_stat("maxHp")

    def get_stat(self, stat):
        value = self.stats[stat]
        if self.weapon is not None:
            value += self.weapon.get_stat(stat)
        if self.armorEquiped is not None:
            value += getattr(self.armorEquiped, stat)
        if self.accessory is not None:
            value += getattr(self.accessory, stat)
        return value

    def describe(self):
        return "it's " + self.name

    def getMaxHp(self):
        return self.get_stat("maxHp")

    def getMaxDamage(self):
        return self.get_stat("maxDamage")

    def getMinDamage(self):
        return self.get_stat("minDamage")

    def getDefense(self):
        return self.get_stat("defense")

    def getArmorStat(self):
        return self.get_stat("armorStat")

    def getSpeed(self):
        return self.get_stat("speed")