from code import terminal, game
from config import colors
from player import player
from menu import menu
from save import save
import time



# Open the title file and print it to
# the center of the screen.

title_color = colors.title
title_color2 = colors.title_text


title = f"""
{title_color}\033[1m                                                                   \033[0m
{title_color}\033[1m   ______  _______  ______ _     _ _______ __   _ _______ ______   \033[0m
{title_color}\033[1m   |     \ |_____| |_____/ |____/  |______ | \  | |______ |     \  \033[0m
{title_color}\033[1m   |_____/ |     | |    \_ |    \_ |______ |  \_| |______ |_____/  \033[0m
{title_color}\033[1m                                                                   \033[0m
{title_color2}\033[1m                           Version 1.0.0                           \033[0m
{title_color}\033[1m                                                                   \033[0m
{title_color2}\033[1m                      Press <enter> To Continue                    \033[0m
{title_color}\033[1m                                                                   \033[0m
{title_color}\033[1m                                                                   \033[0m
{title_color}\033[1m                                                                   \033[0m
"""


# Initiate Terminal Object

term = terminal.Terminal()


# display title

term.display(title.split("\n"))

term.onward()


# Initiate the Game Object and start the
# game.


if save.save_exists():
	player = save.restore_player()

else:
	player = player.Player()
	


while True:
	choice = menu.main_menu()
	
	if choice == 1:
		game = game.Game(player)
		game.play()
		
	
	elif choice == 2:
		print("PvP is not done yet.")


	elif choice == 3:
		print("Profile is not done yet.")


	elif choice == 4:
		print("Leaderboard is not done yet.")


	elif choice == 5:
		print("No News")


	term.onward()

