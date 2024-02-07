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


    def get_loc_from_player(self, playerX, playerY):
        """Find location based on player location"""

        return [self.x-playerX, self.y-playerY]



    def move_towards_player(self, playerX, playerY, dungeon):
        """Move towards the player"""

        # check if player is in range

        if self.weapon and self.x-self.weapon._range <= playerX <= self.x+self.weapon._range and self.y-self.weapon._range <= playerY <= self.y+self.weapon._range:
            return "attack"


        if self.x-self._range <= playerX <= self.x+self._range and self.y-self._range <= playerY <= self.y+self._range:

            # always move Y axis first

            y = 0
            x = 0

            if self.y > playerY:
                y = -1
            elif self.y < playerY:
                y = 1
            elif self.y == playerY:
                if self.x > playerX:
                    x = -1
                elif self.x < playerX:
                    x = 1

            # check for obstructions:

            if dungeon[self.y+y][self.x+x] != " ":
                y = 0
                x = 0

                # try moving x
                if self.x > playerX:
                    x = -1
                elif self.x < playerX:
                    x = 1
                elif self.x == playerX:
                    if self.y > playerY:
                        y = -1
                    elif self.y < playerY:
                        y = 1


            # If they are still obstructed then stay still

            if dungeon[self.y+y][self.x+x] == " ":
                self.y += y
                self.x += x

                return [x, y]





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

