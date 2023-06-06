

class Shield():
	def __init__(self, name, strength, weakness=None):
		self.name = name
		self.strength = strength
		self.weakness = weakness


def restore(json):
	if json:
		return Shield(json["name"], json["strength"], json["weakness"])



woodenshield = Shield("wooden shield", 50, "fire")
ironshield = Shield("iron shield", 200)