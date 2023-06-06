from code.terminal import Border
from config import colors

popup = Border(
	color=colors.popup_border,
	end=colors.reset,
)


default = Border(" ", " ", " ", " ", " ", " ", " ", " ", color="", end="")