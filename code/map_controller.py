from code import terminal
from code import color
import random, copy
from config import colors
from getkey import getkey, keys
import logger


# SIGHT_RANGE is how far above, below,
# to the left and to the right that the
# player can see. If it is set at 10 the
# map the player can see will be 20x20,
# if this is changed to 11 it will be
# 22x22. 

SIGHT_RANGE = 10





class MapController():
	def __init__(self, map, x, y):
		self.map = map
		self.x = x
		self.y = y
		self.touching = None
		self.last_direction = "still"
		

		self.terminal = terminal.Terminal()
		self.terminal.hide_cursor()

		self.legal_spaces = [" "]
		self.special_spaces = ["t"]

		self.offsetX = 0
		self.offsetY = 0



	def spawn_treasure(self):
		"""Finds a random spot to spawn the treasure at"""
		spawn = self.find_spawn()
		self.map[spawn[0]][spawn[1]] = "t"



	def find_spawn(self):
		"""Finds a valid spawn"""
		while True:
			y = random.randint(0, len(self.map)-1)
			if " " in self.map[y]:
				while True:
					x = random.randint(0, len(self.map[y])-1)
					if self.map[y][x] == " ":
						return (y, x)


	def display(self, topbar=None, enemies=[], highlight=None, select=None):
		"""Builds a `display map` and then prints it to the screen"""
		
		self.touching = None


		# Place the player on the map
		self.map[self.y][self.x] = "p"


		# Place enemies
		for enemy in enemies:
			self.map[enemy.y][enemy.x] = enemy.symbol


		# get the "display map" which is the section
		# of the map the player can see. Since printing
		# the whole map would be way to big for the
		# terminal 
		
		display_map = self.build_display_map()


		# terminal.refresh() clears the screen without
		# actually clearing it, it just prints new stuff
		# on top of it. It makes things flicker less, but
		# can sometimes result with things printed on
		# top of eachother
		
		self.terminal.refresh()


		# All characters are converted to being 3
		# characters wide, which keeps the map about
		# squareish instead of having it really skinny
		# and tall
		# A few of the characters are turned into custom
		# characters with colors such as the player or
		# treasure, others just default to having a space
		# slapped on eather side of them.
		
		results = []

		player_loc = None

		for line in display_map:
			for i in line:
				if i == "p":
					player_loc = [line.index(i), display_map.index(line)]

		
		for y in range(len(display_map)):
			output = ""
			for x in range(len(display_map[y])):

				character = display_map[y][x]

				if highlight:
					if self.in_range(x, y, highlight, player_loc=player_loc):
						h = colors.highlight
						logger.log(str([x, y]))
					else:
						h = ""
				else:
					h = ""

				if select:
					selectX = player_loc[0]+select[0]
					selectY = player_loc[1]+select[1]

					if selectX == x and selectY == y:
						h += colors.select

				
				if character == 'p':
					output += self.by_last_direction()
				elif character == "═":
					output += f"{h}═══{colors.reset}"
				elif character == "╗":
					output += f"{h}═╗ {colors.reset}"
				elif character == "╔":
					output += f"{h} ╔═{colors.reset}"
				elif character == "╝":
					output += f"{h}═╝ {colors.reset}"
				elif character == "╚":
					output += f"{h} ╚═{colors.reset}"
				elif character == ".":
					output += f"{h}{color.rgb([0,0,0], [10,10,10])}   {colors.reset}"
				elif character == "╠":
					output += f"{h} ╠═{colors.reset}"
				elif character == "╣":
					output += f"{h}═╣ {colors.reset}"
				elif character == "╬":
					output += f"{h}═╬═{colors.reset}"
				elif character == "b":
					output += f"{h}{color.rgb([0,0,0], [25,25,25])}   {colors.reset}"
				elif character == 't':
					output += f"{h}\033[93m ⎕ {colors.reset}"
				else:
					output += f"{h} {character} {colors.reset}"

			results.append(output)



		# Display the results

		if topbar:
			results.insert(0, "")
			results.insert(0, topbar)


		self.terminal.display(results, noblink=True, usc=True)


		# make the player disappear so it doesn't leave
		# a trail behind it.
		
		self.map[self.y][self.x] = " "


		# remove any enemies we spawned in

		for enemy in enemies:
			self.map[enemy.y][enemy.x] = " "



	def build_display_map(self):
		"""Cuts the map down to size."""

		# Specify the X and Y range
		
		x_range = (self.x-SIGHT_RANGE, self.x+SIGHT_RANGE)
		y_range = (self.y-SIGHT_RANGE, self.y+SIGHT_RANGE)

		self.offsetX = x_range[0]
		self.offsetY = y_range[0]

		display_map = []


		# cut down the full map to just being without
		# the X and Y range, if the X or Y range
		# extends beyond the actual map, fill it with
		# empty space characters "."
		
		for y in range(y_range[0], y_range[1]):
			line = ["b"]
			if y < 0 or y >= len(self.map):
				for x in range(x_range[0], x_range[1]):
					line.append(".")
			else:
				for x in range(x_range[0], x_range[1]):
					if x < 0 or x >= len(self.map[0]):
						line.append(".")
					else:
						line.append(self.map[y][x])
			line.append("b")
			display_map.append(line)



		# Add borders to the map to make it look nicer
		# then return the cutdown map

		display_map.append("b"*(len(display_map[0])))
		display_map.insert(0, "b"*(len(display_map[0])))
		return display_map


	def get_sub_loc(self, loc):
		"""Return sub location inside of display map"""

		x = loc[0]
		y = loc[1]

		return [x+self.offsetX, y+self.offsetY]
				
		
	def by_last_direction(self):
		"""Return a character based on the players last direction"""


		# Adds the arrows pointing the way the
		# character is moving.
		
		if self.last_direction == "up":
			return "\033[31m ▲ \033[0m"
		elif self.last_direction == "down":
			return "\033[31m ▼ \033[0m"
		elif self.last_direction == "right":
			return "\033[31m ▶ \033[0m"
		elif self.last_direction == "left":
			return "\033[31m ◀ \033[0m"
		else:
			return "\033[31m ❖ \033[0m"




	# All of these functions are basically
	# the same. They check if the space the
	# player intends to move into is a valid
	# location that they can move to. if it is,
	# it moves them forward by changing their X,Y
	# cordinates

	def move_up(self):
		"""Move the player up"""
		space = self.map[self.y-1][self.x]
		if space in self.legal_spaces:
			self.y -= 1
			self.last_direction = "up"
		elif space in self.special_spaces:
			self.y -= 1
			self.touching = space
			self.last_direction = "still"
		else:
			self.last_direction = "still"

			
	def move_down(self):
		"""move the player down"""
		space = self.map[self.y+1][self.x]
		if space in self.legal_spaces:
			self.y += 1
			self.last_direction = "down"
		elif space in self.special_spaces:
			self.y += 1
			self.touching = space
			self.last_direction = "still"
		else:
			self.last_direction = "still"

			
	def move_right(self):
		"""Move the player right"""
		space = self.map[self.y][self.x+1]
		if space in self.legal_spaces:
			self.x += 1
			self.last_direction = "right"
		elif space in self.special_spaces:
			self.x += 1
			self.touching = space
			self.last_direction = "still"
		else:
			self.last_direction = "still"

			
	def move_left(self):
		"""move the player left"""
		space = self.map[self.y][self.x-1]
		if space in self.legal_spaces:
			self.x -= 1
			self.last_direction = "left"
		elif space in self.special_spaces:
			self.x -= 1
			self.touching = space
			self.last_direction = "still"
		else:
			self.last_direction = "still"




	def in_range(self, x, y, _range, player_loc=None):
		"""Check if an item is in a certain
		range from player"""

		X = self.x
		Y = self.y

		if player_loc:
			X = player_loc[0]
			Y = player_loc[1]

		if x-_range <= X <= x+_range and y-_range <= Y <= y+_range:
			return True

		return False
	


	def select_enemy(self, enemies, player, topbar=None):
		"""Highlight player's range and select
		the enemy"""

		map_copy = copy.deepcopy(self.map)


		# Get enemies in range

		in_range_enemies = []

		for e in enemies:
			if self.in_range(e.x, e.y, player.weapon._range):
				in_range_enemies.append(e)


		if not in_range_enemies:
			self.display(topbar, enemies, highlight=player.weapon._range)
			getkey()
			return False

		index = 0


		while True:
			
			self.display(topbar, enemies, highlight=player.weapon._range, select=in_range_enemies[index].get_loc_from_player(self.x, self.y, self.map))


			logger.log("Displayed map!")


			key = getkey()

			if key not in ["e", "\n"]:
				if index+1 < len(in_range_enemies):
					index += 1
				else:
					index = 0
			
			elif key == "\n":
				return in_range_enemies[index]

			if key == "e":
				return False
