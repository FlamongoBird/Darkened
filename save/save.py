import json
from player import player

with open('save/save.txt', 'w') as file:file.write("")

def player_to_json(player):
	"""Convert the player object to JSON"""

	JSON = json.loads(json.dumps(player, default=lambda o: o.__dict__))

	return JSON




def player_from_json(json):
	"""Convert JSON back into a player"""

	p = player.Player()
	p.restore(json)
	return p



def save_player(player):
	"""Save player data"""

	with open("save/save.txt", "w") as file:
		file.write(json.dumps(player_to_json(player)))



def restore_player():
	"""Restore Player"""

	with open("save/save.txt", "r") as file:
		data = json.loads(file.read())

	return player_from_json(data)



def save_exists():
	"""Check if a save exists"""

	with open("save/save.txt", "r") as file:
		data = file.read()

	if data:
		return True

	return False