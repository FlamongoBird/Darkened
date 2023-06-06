from code import terminal
from config import colors, borders

main = f"""
{colors.title}\033[1m                                                                   \033[0m
{colors.title}\033[1m   ______  _______  ______ _     _ _______ __   _ _______ ______   \033[0m
{colors.title}\033[1m   |     \ |_____| |_____/ |____/  |______ | \  | |______ |     \  \033[0m
{colors.title}\033[1m   |_____/ |     | |    \_ |    \_ |______ |  \_| |______ |_____/  \033[0m
{colors.title}\033[1m                                                                   \033[0m
{colors.title}\033[1m                                                                   \033[0m



""".split("\n")

term = terminal.Terminal()

def main_menu():
	path = ["Main"]
	while True:
		main[-3] = f"{colors.menu_path}{'>'.join(path)}{colors.reset}"
		choice = term.get_input(
			"prompt", 
			main, 
			border=borders.default,
			prompts=[
				["Dungeons", 1],
				["PvP", 2],
				["Profile", 3],
				["Leaderboard", 4],
				["News", 5],
				["Exit", "e"],
			],
			align="right",
			selector=f"{colors.selector}>"
		)

		if choice == "e":
			exit("Thanks for playing!")
		else:
			return choice