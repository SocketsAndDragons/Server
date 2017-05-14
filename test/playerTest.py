"""
Author: Thomas Bonatti (thomasbonatti2695@gmail.com)
"""

import unittest
from Server.server.player import Player
from Server.server import room


class MapTest(unittest.TestCase):

    def setUp(self):
        self.player = Player(1, "Mr. Test", "0123456789")

    def tearDown(self):
        pass

    def testHealHeals(self):
        self.player.wounds = 5
        self.player.heal_damage(2)
        self.assertEqual(self.player.wounds, 3)

    def testHealDoesntOverheal(self):
        self.player.wounds = 2
        self.player.heal_damage(5)
        self.assertEqual(self.player.wounds, 0)

    def testHealDoesntHarm(self):
        self.player.wounds = 0
        self.player.heal_damage(-5)
        self.assertEqual(self.player.wounds, 0)

    def testDamageDealsDamage(self):
        self.player.wounds = 2
        self.player.deal_damage(self.player.get_stat('armor') + 5)
        self.assertEqual(self.player.wounds, 7)

    def testDamageDoesntHeal(self):
        self.player.wounds = 1
        self.player.deal_damage(self.player.get_stat('armor') - 4)
        self.assertEqual(self.player.wounds, 1)

    def testGetStat(self):
        expected = self.player.stats['maxHp']
        received = self.player.get_stat("maxHp")
        self.assertEqual(expected, received)


if __name__ == "__main__":
    unittest.main()