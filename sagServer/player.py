

class Player:

    def __init__(self):

        self.weapon
        self.armor
        self.accessory
        self.maxHp
        self.wounds
        self.atcDamage
        self.defense
        self.armor
        self.speed

    def healDamage(self, healing):
        if healing < 0: return False

        self.wounds -= healing
        if self.wounds <= 0:
            self.wounds = 0

        return True

    def dealDamage(self, damage):
        total_damage = damage-self.getArmor()
        if total_damage < 0: return False

        self.wounds += total_damage
        return True

    def getHpLeft(self):
        return self.getMaxHp() - self.wounds

    def getMaxHp(self):
        maxHp = self.maxHp
        maxHp += self.weapon.maxHp
        maxHp += self.armor.maxHp
        maxHp += self.accessory.maxHp
        return maxHp

    def getAtcDamage(self):
        dmg = self.atcDamage
        dmg += self.weapon.atcDamage
        dmg += self.armor.atcDamage
        dmg += self.accessory.atcDamage
        return dmg

    def getDefense(self):
        defns = self.defense
        defns += self.weapon.defense
        defns += self.armor.defense
        defns += self.accessory.defense
        return defns

    def getArmor(self):
        armor = self.armor
        armor += self.weapon.armor
        armor += self.armor.armor
        armor += self.accessory.armor
        return armor

    def getSpeed(self):
        spd = self.speed
        spd += self.weapon.speed
        spd += self.armor.speed
        spd += self.accessory.speed
        return spd