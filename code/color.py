
def rgb(fg=[], bg=[]):
    """Builds a custom color from an RGB Value"""
    color = ""
    if fg:
    	color += f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m"
    if bg:
    	color += f"\033[48;2;{bg[0]};{bg[1]};{bg[2]}m"
    return color


def color(self, string, fg=None, bg=None, end="\033[0m"):
	return f"{custom(fg, bg)}{string}{end}"
