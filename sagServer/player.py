
STARTING_HP = 20
STARTING_ACC = 90
STARTING_MAX_DMG = 6
STARTING_MIN_DMG = 2
STARTING_DEF = 10
STARTING_ARM = 0
STARTING_SPD = 5


class Player:

    def __init__(self, number, name):

        self.number = number
        self.name = name

        self.weapon = None
        self.armorEquiped = None
        self.accessory = None
        self.wounds = 0
        self.maxHp = STARTING_HP
        self.accuracy = STARTING_ACC
        self.maxDamage = STARTING_MAX_DMG
        self.minDamage = STARTING_MIN_DMG
        self.defense = STARTING_DEF
        self.armorStat = STARTING_ARM
        self.speed = STARTING_SPD

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
        return self.getStat("maxHp")

    def getStat(self, stat):
        stat = getattr(self, stat)
        if self.weapon is not None:
            stat += getattr(self.weapon, stat)
        if self.armorEquiped is not None:
            stat += getattr(self.armorEquiped, stat)
        if self.accessory is not None:
            stat += getattr(self.accessory, stat)
        return stat

    def getMaxHp(self):
        return self.getStat("maxHp")

    def getMaxDamage(self):
        return self.getStat("maxDamage")

    def getMinDamage(self):
        return self.getStat("minDamage")

    def getDefense(self):
        return self.getStat("defense")

    def getArmorStat(self):
        return self.getStat("armorStat")

    def getSpeed(self):
        return self.getStat("speed")