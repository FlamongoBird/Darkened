from code import terminal


term = terminal.Terminal()



"""
Future Goals:

Upgrade weapons stats and merge with
Magic items. For example:
sword + fire orb = Fire Sword I

Current Goals:

Used to repair items
"""



def forge():
	while True:
		choice = term.get_input("prompt", "Forge", [("Exit", "e")])

		if choice == "e":
			return
