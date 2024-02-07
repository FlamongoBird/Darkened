from weapons import weapons, armors, shields
import random

class Enemy():
    """Enemy class"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.alive = False


    def spawn(self, _map):
        """Finds a suitable spawn for the enemy"""
        self.y, self.x = _map.find_spawn()

    def move(self, _map, player):
        """Moves towards the player if the player is within range"""
        return





class Monster(Enemy):
    def __init__(self, name, hp, weapon, armor, shield, _type, parts, symbol="e", _range=10, ammo=[]):
        super().__init__()

        self.name = name
        self.hp = hp
        self.weapon = weapon
        self.armor = armor
        self.shield = shield
        self.symbol = symbol
        self._range = _range
        self._type = _type
        self.parts = parts
        self.ammo = ammo




def gen_goblin():
    goblindagger = weapons.Weapon("goblin dagger", 5, 2, 7, 2)
    goblinchainmail = armors.Armor("goblin chainmail", 5, [])
    goblinshield = shields.Shield("wooden shield", 25, "fire")
    return Monster("Goblin", 10, goblindagger, goblinchainmail, goblinshield, "goblin", "head", "G", 5)

