from weapons import weapons


class Companion():
	def __init__(self):
		self.name = ""
		self.weapon = None
		self.armor = None
		self.shield = None
		self.hp = 20
		self.max_hp = 20
		self.alive = True