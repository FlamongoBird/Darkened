
class Border():
	def __init__(self, top="═", bottom="═", left="║", right="║", toprightcorner="╗", topleftcorner="╔", bottomrightcorner="╝", bottomleftcorner="╚", color="", end="\033[0m"):
		"""Inits a border"""
		self.top = color+top+end
		self.bottom = color+bottom+end
		self.left = color+left+end
		self.right = color+right+end
		self.toprightcorner = color+toprightcorner+end
		self.topleftcorner = color+topleftcorner+end
		self.bottomrightcorner = color+bottomrightcorner+end
		self.bottomleftcorner = color+bottomleftcorner+end