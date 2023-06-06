from getkey import getkey, keys
from code import map_controller, loot, die, dungeon
from enemies import enemy
from battle import battle
from save import save
from config import colors, borders



class Game():
	def __init__(self, player):
		"""Intiate the Game object"""

		self.dungeon = dungeon.build_dungeon()

		self.player = player

		self.x = self.dungeon[1][0]
		self.y = self.dungeon[1][1]
		
		self.map = map_controller.MapController(self.dungeon[0], self.x, self.y)
 
		self.map.spawn_treasure()

		self.enemies = []
			

		


	def play(self):
		"""Runs the main loop, displaying the map and 
			taking input for moves from the player"""
		sc = 0

		while True:
			sc += 1
			if sc == 10:
				save.save_player(self.player)
				sc = 0

			# Display the map
			
			self.map.display(self.player.quick_stats(), self.enemies)


			# Get a key input from the player
			
			key = getkey()


			# Move the player
			
			if key == "w" or key == keys.UP:
				self.map.move_up()
			elif key == "s" or key == keys.DOWN:
				self.map.move_down()
			elif key == "d" or key == keys.RIGHT:
				self.map.move_right()
			elif key == "a" or key == keys.LEFT:
				self.map.move_left()



			elif key == "1":
				self.player.full_stats()


			# check if player wants to attack

			elif key == "f":
				if not self.player.weapon:
					text = "No weapon equipped!"
					continue


				e = self.map.select_enemy(self.enemies, self.player, self.player.quick_stats())

				if e:
					self.map.terminal.popup(colors.fancify(battle.attack(self.player, e)), pause=0.01, border=borders.popup)
					self.map.terminal.onward()

					if e.hp < 1:
						self.map.display(self.player.quick_stats(), self.enemies)
						e.alive = False
						self.enemies.remove(e)
						self.map.terminal.popup(colors.fancify(f"*{e.name}* has died."), pause=0.01, border=borders.popup)
						self.map.terminal.onward()




			elif key == "t":
				#self.map.spawn_treasure()

				e = enemy.gen_goblin()
				e.alive = True
				e.spawn(self.map.map)
				self.enemies.append(e)



			# move enemies:

			for e in self.enemies:
				if e.alive:
					cords = e.move_towards_player(self.map.x, self.map.y, self.map.map)
					if cords == "attack":
						dmg = e.weapon.damage
						self.player.hp -= dmg
						self.map.terminal.popup(colors.fancify(f"*{e.name}* attacked you!\n{e.name} dealt *{dmg}* damage!"), pause=0.01, border=borders.popup)
						self.map.terminal.onward()

						if self.player.hp < 1:
							self.map.display(self.player.quick_stats(), self.enemies)
							self.map.terminal.popup(colors.fancify(f"You have *died*."), pause=0.01, border=borders.popup)
							self.map.terminal.onward()
							die.die(f"Slayed by {e.name}")

				

				
			# check if the player is touching 
			# the treasure, which is the win 
			# condition 
				
			if self.map.touching == "t":
				self.map.terminal.popup(colors.fancify(loot.open_chest(self.player)), pause=0.01, border=borders.popup)
				self.map.terminal.onward()



	def win(self):
		"""Displays the win screen"""
		with open("assets/win.txt", "r") as file:
			win_screen = file.read().split("\n")
		self.map.terminal.clear()
		self.map.terminal.display(win_screen)
		exit()
