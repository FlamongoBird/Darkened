

class Armor():
	def __init__(self, name, armor, protects):
		self.name = name
		self.armor = armor
		self.protects = protects


def restore(json):
	if json:
		return Armor(json["name"], json["armor"], json["protects"])


# leather armor: 1-3 pen
# chain mail: 4-8 pen
# plate armor: 12-20 pen

hardenedleather = Armor("leather armor", 1, ["fire"])

chainmail = Armor("chainmail", 4, [])

platearmor = Armor("plate armor", 15, [])