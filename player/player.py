from config import colors, borders
from weapons import weapons, armors, shields
from code import terminal

term = terminal.Terminal()

class Ammo():
	def __init__(self, name, _type, damage, armor_pen, speed, effects=None):
		self.name = name
		self.damage = damage
		self.effects = effects
		self.armor_pen = armor_pen
		self.speed = speed
		self._type = _type

ironball       = lambda: Ammo("iron ball",       "shot",  30, 50, 11)

class Inventory():
	def __init__(self):
		self.weapons = []
		self.armors = []
		self.shields = []
		self.items = []
		self.weapon_items = []
		self.current_weight = 0
		self.max_weight = 20
		self.arrows = []
		self.gold = 0
		self.silver = 0
		self.diamonds = 0
		self.ammo = [ironball(), ironball(), ironball()]


	def quick_stats(self):
		return [
			f"Gold: {self.gold}",
			f"Silver: {self.silver}",
			f"Diamonds: {self.diamonds}",
		]


	def restore(self, json):
		self.weapons = [weapons.restore(weapon) for weapon in json["weapons"]]
		self.armors = [armors.restore(armor) for armor in json["armors"]]
		self.shields = [shields.restore(shield) for shield in json["shields"]]
		self.items = json["items"]
		self.weapon_items = json["weapon_items"]
		self.current_weight = json["current_weight"]
		self.max_weight = json["max_weight"]
		self.arrows = json["arrows"]
		self.gold = json["gold"]
		self.silver = json["silver"]
		self.diamonds = json["diamonds"]
		self.ammo = json["ammo"]
		



	def has_ammo(self, ammo_selected):
		for ammo in self.ammo:
			if ammo.name == ammo_selected:
				return True


	def use_ammo(self, ammo_selected):
		for ammo in self.ammo:
			if ammo.name == ammo_selected:
				self.ammo.remove(ammo)
				return ammo


	def count_ammo(self, ammo_selected):
		count = 0
		for ammo in self.ammo:
			if ammo.name == ammo_selected:
				count += 1

		return count



class Companions():
	def __init__(self):
		self.companions = []

	def restore(self, json):
		self.companions = json["companions"]


class PVP():
	def __init__(self):
		self.trophies = 0
		self.rank = "Challenger" # Gladiator, Knight, Champion
		self.wins = 0
		self.losses = 0
		


class Player():
	def __init__(self):
		self.name = ""
		self.level = 1
		self.xp = 0
		self.xp_next = 10
		self.inventory = Inventory()
		self.weapon = weapons.cannon.build("nivorion")
		self.selected_ammo_type = "shot"
		self.armor = None
		self.shield = None
		self.hp = 20
		self.max_hp = 20
		self.companions = Companions()

		# PVP

		#self.pvp = PVP()

	def full_stats(self):
		"""Return full player stats"""

		content = [
			f"Name: {self.name}",
			f"Level: {self.level}",
			f"XP: {self.xp}/{self.xp_next}",
			f"Weapon: {self.weapon.name if self.weapon else None}",
			f"Armor: {self.armor.name if self.armor else None}",
			f"Shield: {self.sheild.name if self.shield else None}",
		]

		content += self.inventory.quick_stats()

		term.popup(content, pause=False, border=borders.popup)

		term.onward()



	def restore(self, json):
		self.name = json["name"]
		self.level = json["level"]
		self.xp = json["xp"]
		self.xp_next = json["xp_next"]
		self.inventory = Inventory()
		self.inventory.restore(json["inventory"])
		self.weapon = weapons.restore(json["weapon"])
		self.selected_ammo_type = json["selected_ammo_type"]
		self.armor = armors.restore(json["armor"])
		self.shield = shields.restore(json["shield"])
		self.hp = json["hp"]
		self.max_hp = json["max_hp"]
		self.companions = Companions()
		self.companions.restore(json["companions"])


	def quick_stats(self):
		percent = (self.hp/self.max_hp)*100
		if percent < 25:
			color = colors.hp_bad
		elif percent < 50:
			color = colors.hp_meh
		else:
			color = colors.hp_good

		# maybe switch to use hearts?
		hp = f"{color}█"*self.hp
		if self.hp != self.max_hp:
			hp += f"{colors.hp_gone}█"*(self.max_hp-self.hp)
		hp += colors.reset
		if self.weapon.ammo_types:
			count = self.inventory.count_ammo(self.selected_ammo_type)
			extra = "ammo: "+("|" * count if count else "None")
		else:
			extra = ""
		return f"hp: {hp}  xp: {self.xp}/{self.xp_next}  {extra}"


	def get_stats(self):
		output = []
		output.append(self.quick_stats)
		
		if self.weapon:
			output.append(self.weapon.stats())

		if self.armor:
			output.append(self.armor.stats())

		if self.shield:
			output.append(self.shield.stats())
		