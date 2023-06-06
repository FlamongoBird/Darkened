from code.color import rgb
from code.border import Border

reset = "\033[0m"
title = rgb([225, 0, 0])
title_text = rgb([163, 163, 163])
menu_path = rgb([150, 0, 0])+"\033[1m\033[4m"



hp_good = rgb([0, 180, 0])
hp_meh = rgb([160, 90, 10])
hp_bad = rgb([160, 0, 0])
hp_gone = rgb([30, 30, 30])




highlight = rgb(bg=[30, 30, 30])
select = "\033[7m"



selector = rgb(bg=[30, 30, 30])



popup_border = rgb(fg=[30, 30, 30])



silver = rgb(fg=[192, 192, 192])
gold = rgb(fg=[212, 175, 55])
diamond = rgb(fg=[27, 226, 255])





special_color = rgb(fg=[255, 0, 0])
int_color = rgb(fg=[255, 0, 0])

def fancify(string):

	x = ""

	coloring = ""

	for i in string:
		if i == "*":
			if coloring:
				x += "\033[0m"
				coloring = ""
			else:
				coloring = special_color
		else:
			x += coloring+i


	return x
