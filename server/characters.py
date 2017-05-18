
import dungeon_server
from server import items
from random import randint

# STARTING_HP = 20
# STARTING_ACC = 90
# STARTING_MAX_DMG = 6
# STARTING_MIN_DMG = 2
# STARTING_DEF = 10
# STARTING_ARM = 0
# STARTING_SPD = 5

BASE_STATS = {
    'maxHp': 25,
    'accuracy': 90,
    'maxDamage': 6,
    'minDamage': 2,
    'defense': 10,
    'armor': 0,
    'speed': 5,
    'deaths': 0
}

class DeadBody:

    def __init__(self, killed):
        self.name = killed.name + "'s mangled corpse"

    def describe(self):
        return self.name + " stares through the darkness into your soul."

    def action_used(self, actor, current_room):
        return  [{
            "message": "the hollow eyes of the recently deceased " + self.name + " watch you still...",
            "dest": {
                "type": "uuid",
                "value": actor.uuid
            }
        }]


class Death:

    def __init__(self, killed, attacker=None):
        self.attacker = attacker
        self.killed = killed

    def get_msg(self):
        msg = self.killed.name + " was killed"
        if self.attacker is not None:
            msg += " by " + self.attacker.name
        return msg

    def __str__(self):
        return self.get_msg()

    def __repr__(self):
        return self.get_msg()

    def try_adding_equipment(self, inv, slot_name):
        if hasattr(self.killed, slot_name):
            slot = getattr(self.killed, slot_name)
            if slot is not None:
                inv.add_item(slot)

    def handle_death(self):
        server = dungeon_server.Server()
        x, y = server.map.findEntityByName(self.attacker.name)
        current_room = server.map.get_room(x, y)

        if hasattr(self.killed, "inventory"):
            inv = self.killed.inventory
        else:
            inv = items.ItemContainer("dropped items")

        self.try_adding_equipment(inv, "weapon")
        self.try_adding_equipment(inv, "armor_equiped")
        self.try_adding_equipment(inv, "accessory")

        current_room.entities.remove(self.killed)
        current_room.entities.append(DeadBody(self.killed))

        events = []
        events.append(self.base_event())
        if not len(inv.items) == 0:
            current_room.entities.append(inv)
            events.append({
                "message": self.killed.name + " dropped some items in the room.",
                "dest": {
                    "type": "room",
                    "x": x,
                    "y": y
                }
            })
        if hasattr(self.killed, 'uuid'):
            events.append(self.respawn_player())

        return events

    def base_event(self):
        return {
            "message": self.get_msg(),
            "dest": {"type": "all"}
        }

    def respawn_player(self):
        server = dungeon_server.Server()
        n_deaths = self.killed.get_stat("deaths") + 1
        server.register_new_player(self.killed.uuid, times_killed=n_deaths)
        return {
            "message": "you respawned as " + server.players[self.killed.uuid].name,
            "dest": {
                "type": "uuid",
                "value": self.killed.uuid
            }
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
        if total_damage < 0: return 0
        self.wounds += total_damage
        return total_damage

    def get_hp_left(self):
        return self.get_stat('maxHp') - self.wounds

    def action_used(self, actor, current_room):
        return []

    def attack(self, target):
        defense = target.get_stat("defense")
        acc = self.get_stat("accuracy")
        effectve_acc = acc - defense
        result = {}
        rn = randint(1, 100)
        if rn == 1 or rn <= effectve_acc:
            dmg = randint(self.get_stat("minDamage"), self.get_stat(("maxDamage")))
            result["damage"] = target.deal_damage(dmg)
            result["hit"] = True
            if target.wounds >= target.get_stat("maxHp"):
                death = Death(target, attacker=self)
                event = death.handle_death()
                result["death"] = event

        else:
            result["damage"] = 0
            result["hit"] = False
        return result

    def default_attack_events(self, target, result):
        if result["hit"]:
            final_dmg = result["damage"]
            attacker_msg = "You hit " + target.name + " and dealt " + str(final_dmg) + " damage."
            target_msg = "You were hit by " + self.name + " and dealt " + str(final_dmg) + " damage."
            observer_msg = target.name + " was hit by " + self.name + " and dealt " + str(final_dmg) + " damage."
        else:
            attacker_msg = target.name + "evaded your attack!"
            target_msg = "You evaded an attack from " + self.name
            observer_msg = target.name + " evaded an attack from " + self.name

        events = []
        exclude = []
        if hasattr(self, "uuid"):
            events.append({
                "result": result,
                "message": attacker_msg,
                "dest": {
                    "type": 'uuid',
                    "value": self.uuid
                }
            })
            exclude.append(self.uuid)
        if hasattr(target, "uuid"):
            events.append({
                "result": result,
                "message": target_msg,
                "dest": {
                    "type": "uuid",
                    "value": target.uuid
                }
            })
            exclude.append(target.uuid)
        if "death" in result:
            events += result['death']

        x, y = dungeon_server.Server().map.findEntityByName(self.name)
        events.append({
            "result": result,
            "message": observer_msg,
            "dest": {
                "type": 'room',
                "x": x,
                "y": y,
                "exclude": exclude
            }
        })
        return events

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
        self.armor_equipped = None
        self.accessory = None

    def __repr__(self):
        return self.name + "(player " + str(self.number) + ")"

    def receive_item(self, item):
        self.inventory.add_item(item)

    def get_stat(self, stat):
        value = self.stats[stat]
        if self.weapon is not None:
            value += self.weapon.get_stat(stat)
        if self.armor_equipped is not None:
            value += self.armor_equipped.get_stat(stat)
        if self.accessory is not None:
            value += self.accessory.get_stat(stat)
        return value

    def describe(self):
        return "it's " + self.name


class Monster(Character):

    def __init__(self, name, loot=None, **starting_stats):
        super(Monster, self).__init__(name, starting_stats)
        if loot is not None:
            self.inventory = loot

    def describe(self):
        return self.display_stats()

    def action_used(self, actor, current_room):
        result = self.attack(actor)
        events = self.default_attack_events(actor, result)
        return events

