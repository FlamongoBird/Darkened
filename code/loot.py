import random
from config import colors
from code import die

## loot:
"""
LOOT FORMAT: 
{
	"name" : "<name>",
	"value" : "<value>",
	"_type" : "<_type>", ie: gold, diamonds, silver, weapon, armor, shield, scorpion
	"rarity" : "<rarity>" value out of 1000
}
"""

chestloot = ["silver", "gold", "diamonds", "shield", "armor", "weapon", "scorpion"]
chestchance = [500, 200, 100, 50, 50, 50, 50]


def open_chest(player):
	loot = random.choices(chestloot, weights=chestchance, k=1)[0]

	if loot == "silver":
		i = random.randint(10, 30)
		player.inventory.silver += i
		return f"You found {colors.silver}{i}{colors.reset} silver coins"

	elif loot == "gold":
		i = random.randint(2, 8)
		player.inventory.gold += i
		return f"You found {colors.gold}{i}{colors.reset} gold coins"

	elif loot == "diamonds":
		i = random.randint(1, 2)
		player.inventory.diamonds += i
		return f"You found {colors.diamond}{i}{colors.reset} diamond{'s' if i != 1 else ''}"

	elif loot == "shield":
		return f"You found a shield"

	elif loot == "weapon":
		return f"You found a weapon"

	elif loot == "armor":
		return f"You found armor"

	else:
		player.hp -= 4
		if player.hp < 1:
			die.die("Killed by a scorpion lol")
		return f"A scorpion leaps out and stings you\n*-4* hp"


	return f"You found *{loot}*"