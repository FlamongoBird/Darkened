from code import terminal
class Battle():
    """A battle between the player and opponent(s)"""
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies

        self.terminal = terminal.Terminal()
    

    def battle(self):
        """Do the battle"""



def attack(player, enemy):
    """Deal damage to an enemy"""

    if not player.weapon:
        return "You have no weapon equipped."


    dmg = 0
    pen = 0
    speed = 0

    if player.weapon.ammo_types:
        if player.inventory.has_ammo(player.selected_ammo_type):
            ammo = player.inventory.use_ammo(player.selected_ammo_type)

            pen = ammo.armor_pen

            speed = ammo.speed

            dmg = player.weapon.damage * ammo.damage

        else:
            return "You are out of ammo."

    else:
        dmg = player.weapon.damage
        pen = player.weapon.armor_pen
        speed = player.weapon.speed


    # if enemy.speed > speed: dodge=random.randint(1, 2)

    if enemy.armor and enemy.armor.armor > pen:
        return f"You attack does not peirce *{enemy.name}*'s armor"


    enemy.hp -= dmg


    return f"You attack *{enemy.name}*\nYour attack deals *{dmg}* damage\n*{enemy.name}* now has *{enemy.hp}* hp"