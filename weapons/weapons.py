import random


def rand(_tuple):
	return random.randint(_tuple[0], _tuple[1])

class WeaponClass():
	def __init__(self, classname, dmg_range, pen_range, speed_range, _range, required_ammo=None):
		self.classname = classname
		self.dmg_range = dmg_range
		self.pen_range = pen_range
		self.speed_range = speed_range
		self._range = _range
		self.required_ammo = required_ammo


	def calc_tier(self, weapon):
		return 1


	def build(self, name):
		w = Weapon(
			name=f"{name} {self.classname}",
			damage=rand(self.dmg_range),
			armor_pen=rand(self.pen_range),
			speed=rand(self.speed_range),
			_range=rand(self._range),
			ammo_types=self.required_ammo
		)
		w.name += f" {'I' * self.calc_tier(w)}"

		return w




### WEAPON CLASSES ###

##                        WEAPON NAME    DMG         PEN      SPEED     RANGE    AMMO

dagger = WeaponClass(         "dagger", [2, 3],     [1, 1],   [5, 8],   [1, 2],  None)
shortsword = WeaponClass("short sword", [3, 5],     [1, 2],   [4, 6],   [2, 3],  None)
longsword = WeaponClass(  "long sword", [6, 8],     [2, 5],   [3, 5],   [3, 3],  None)
battleaxe = WeaponClass(  "battle axe", [8, 13],    [5, 10],  [2, 3],   [3, 3],  None)
warhammer = WeaponClass(  "war hammer", [6, 9],     [10, 18], [2, 3],   [3, 3],  None)
armcannon = WeaponClass(  "arm cannon", [1, 1],     [1, 1],   [1, 1],   [6, 7], ["shot"])
cannon = WeaponClass(         "cannon", [4, 4],     [2, 2],   [2, 2],   [9, 9], ["shot"])
recurvebow = WeaponClass("recurve bow", [.75,1],    [1, 1],   [1, 1],   [4, 5], ["arrow"])
longbow = WeaponClass(       "longbow", [1, 1],     [1, 1],   [1, 1],   [6, 7], ["arrow"])
crossbow = WeaponClass(     "crossbow", [1.2, 1.5], [1, 1.1], [1, 1.1], [7, 8], ["bolt"])
blowgun = WeaponClass(      "blow gun", [1, 1],     [1, 1],   [1, 1],   [4, 5], ["dart"])



class Weapon():
	def __init__(self, name, damage, armor_pen, speed, _range=0, ammo_types=None, integrity=100):
		self.name = name
		self.damage = damage
		self.armor_pen = armor_pen
		self.speed = speed
		self._range = _range
		self.ammo_types = ammo_types
		self.integrity = integrity
		self.max_integrity = integrity


	def forge(self, weapon):
		pass


class Ammo():
	def __init__(self, name, _type, damage, armor_pen, speed, effects=None):
		self.name = name
		self.damage = damage
		self.effects = effects
		self.armor_pen = armor_pen
		self.speed = speed
		self._type = _type


def restore_ammo(json):
	if json:
		return Ammo(json["name"], json["_type"], json["damage"], json["armor_pen"], json["speed"], json["effects"])

def restore(json):
	if json:
		return Weapon(json["name"], json["damage"], json["armor_pen"], json["speed"], json["_range"], json["ammo_types"], json["integrity"], json["max_integrity"])



# leather armor: 1-3 pen
# chain mail: 4-8 pen
# plate armor: 12-20 pen

## Ammos ##

blowdart       = lambda: Ammo("blowdart",        "dart",  5,   0, 9)
poisondart     = lambda: Ammo("poison blowdart", "dart",  20,  0, 9, effects=["poison"])
stundart       = lambda: Ammo("stun dart",       "dart",  1,   0, 9, effects=["stun"])

arrow          = lambda: Ammo("arrow",           "arrow", 15,  5, 8)
poisonarrow    = lambda: Ammo("poison arrow",    "arrow", 30,  5, 8, effects=["poison"])
firearrow      = lambda: Ammo("fire arrow",      "arrow", 25,  5, 8, effects=["fire"])
broadheadarrow = lambda: Ammo("broadhead arrow", "arrow", 20,  5, 8)
bodkinarrow    = lambda: Ammo("bodkin arrow",    "arrow", 15, 10, 8)

stone          = lambda: Ammo("stone",           "shot",  20,  8, 11)
pebbles        = lambda: Ammo("pebbles",         "shot",  10,  5, 11, effects=["spread"])

ironball       = lambda: Ammo("iron ball",       "shot",  30, 50, 11)
