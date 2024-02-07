

"""
████████ █████████ ████████ ████   ███  ███████ ███  ███
███▀▀▀▀▀ ▀▀▀███▀▀▀ ███▀▀▀▀▀ █████  ███ ███▀▀▀▀▀ ███  ███
████████    ███    ██████   ██████ ███ ███      ████████
▀▀▀▀▀███    ███    ███▀▀▀   ███▀██████ ███      ███▀▀███
████████    ███    ████████ ███ ▀█████ ▀███████ ███  ███
▀▀▀▀▀▀▀▀    ▀▀▀    ▀▀▀▀▀▀▀▀ ▀▀▀  ▀▀▀▀▀  ▀▀▀▀▀▀▀ ▀▀▀  ▀▀▀

My glorious masterpeice, my work of art!

Built to make Python Text games easier, faster, and more
fun to make.


WARNING: The code below is horrific. I'll just leave it
as that. 
"""


import os, sys, cursor, copy, re, sys, time
from getkey import getkey, keys


from code.border import Border
from code.color import rgb, color


class Terminal():
	def __init__(self):
		"""Inits terminal object"""
		self.width = 0
		self.height = 0
		self.cursor_hidden = False

		self.hide_cursor()

	

	def update_term_size(self):
		"""Update Terminal Size"""

		# get the size of the terminal
		
		size = os.get_terminal_size()


		# if the size has changed clear the screen

		if size.columns != self.width or size.lines != self.height:
			self.clear()


		# store the new size

		self.width = size.columns
		self.height = size.lines


	def center(self, string, width):
		"""Return a centered string based on a width"""

		length_of_string = self.countchars(string)

		padding = (width-length_of_string) // 2

		return (" "*padding)+string



	def countchars(self, string):
		"""Basically len() but disregards chars in self.colors"""
		return len(self.stripcolor(string))


	
	def stripcolor(self, string):
		regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		return regex.sub("", string)


	
	def stripcolors(self, strings):
		"""strips colors from strings"""

		# does what stripcolor does but for a list of
		# strings. I should probably delete this but some
		# code below relies on it.

		output = []

		escape_sequences = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

		for string in strings:
			if type(string) == str:
				output.append(escape_sequences.sub('', string))
			else:
				output.append(string)

		return output



	def balance_strings(self, strings, align="center", usc=False):
		"""Makes all strings the same length"""

		# find the longest string

		longest = self.countchars(max(strings, key=self.countchars))


		# make all strings the same length as the longest

		balanced_strings = []

		if align == "center":
			for string in strings:
				if usc:
					balanced_strings.append((" "*((longest - self.countchars(string)) // 2)) + string)
				else:
					balanced_strings.append(string.center(longest))


		elif align == "right":
			for string in strings:
				balanced_strings.append(string+(" "*(longest-self.countchars(string))))

		elif align == "left":

			for string in strings:
				balanced_strings.append((" "*(longest-self.countchars(string)))+string)

		else:
			return balance_strings(strings)



		# return the results

		return balanced_strings



	def popup(self, content, pause=0.01, border=Border(), _width=None, _height=None):
		"""Display string or list in center of screen"""

		if type(content) != list:
			content = content.split("\n")


		content = self.balance_strings(content)


		card_width = self.countchars(content[0])+6
		card_height = len(content)



		# the content without breaking text

		width = _width
		height = _height

		if not _width:
			width = card_width+4
		if not _height:
			height = card_height+4

		if card_width > width:
			while True:
				print("Terminal is too small to display content!")
				print("Try resizing then pressing enter to continue")
				self.update_term_size()
				if card_width <= self.width-4:
					break
				else:
					input()


		# get the padding width and height outside
		# the card

		paddingX = (width-card_width) // 2
		paddingY = (height-card_height) // 2


		# add offset incase padding is odd

		offset = 2 if width % 2 == 0 else 3


		# Build strings
		
		# Build strings
		output = [f"{border.topleftcorner}{border.top*(width)}{border.toprightcorner}"]

		topwidth = self.countchars(output[0])
		
		for i in range(paddingY-2):
			output.append(border.left+(" "*(width))+border.right)


		indexes = []

		y = paddingY

		for line in content:
			newline = f"{' '*paddingX} {' '*self.countchars(line)} {' '*paddingX}"
			
			x = paddingX

			mywidth = self.countchars(newline)

			if mywidth != topwidth:
				x = ((topwidth-mywidth)-2)
				if x % 2 == 0:
					zed = int(x/2)
					aed = zed
				else:
					zed = int(x/2)
					aed = int(x - zed)
				x += zed
				newline = f"{' '*zed}{newline}{' '*aed}"

			output.append(f"{border.left}{newline}{border.right}")

			indexes.append([y, x])
			y += 1


		for i in range(paddingY-2):
			output.append(border.left+(" "*(width))+border.right)
		
		output.append(f"{border.bottomleftcorner}{border.bottom*(width)}{border.bottomrightcorner}")




		paddingX = (self.width - self.countchars(output[0])) // 2
		paddingY = (self.height - len(output)) // 2


		for i in output:
			self.move_cursor(paddingY, paddingX)
			paddingY += 1
			print(i, end="")



		for index in range(len(content)):
			pos = indexes[index]
			self.move_cursor(pos[0]+(paddingY-(height-1)), pos[1]+paddingX)
			if pause:
				self.typewriter(content[index], pause, end="")
			else:
				print(content[index], end="")




	def display(self, content, noblink=False, balanced=False, align="center", usc=False):
		"""Displays content in str or list format"""

		# clear screen

		if noblink:
			self.refresh()
		else:
			self.clear()


		# make sure type is list

		if type(content) == str:
			content = content.split("\n")


		# update terminal size

		self.update_term_size()


		# check if strings are already balanced. This is
		# only important if displaying strings from display_card
		# or display_table

		if not balanced:
			content = self.balance_strings(content, align, usc)


		# find the padding that needs to be added to center the
		# content in the terminal

		if align == "center":
			paddingX = (self.width - self.countchars(content[0])) // 2
		elif align == "right":
			paddingX = (self.width - self.countchars(content[0]))
		elif align == "left":
			paddingX = 0
		paddingY = (self.height - len(content)) // 2


		# print each line of content

		offsetY = 0


		for line in content:
			self.move_cursor(paddingY+offsetY, paddingX)
			print(line)
			offsetY += 1



	def display_card(self, content, width=None, height=None, border=Border(), noblink=False, showsidebar=False, balanced=False):
		"""Display Content in a card (aka with border)"""

		# update terminal size

		self.update_term_size()


		# assert type is list

		if type(content) == str:
			content = content.split("\n")


		# balance content. ie make all strings the
		# same length

		if not balanced:
			content = self.balance_strings(content)


		# find card width and height

		card_width = self.countchars(content[0])+6
		card_height = len(content)


		# check that the terminal is big enough to display
		# the content without breaking text

		if not width:
			width = self.width-4
		if not height:
			height = self.height-4

		if card_width > width:
			while True:
				print("Terminal is too small to display content!")
				print("Try resizing then pressing enter to continue")
				self.update_term_size()
				if card_width <= self.width-4:
					break
				else:
					input()


		# get the padding width and height outside
		# the card

		paddingX = int((width-card_width)/2)
		paddingY = int((height-card_height)/2)

		x = 0


		# Build strings
		output = [f"{border.topleftcorner}{border.top*(width)}{border.toprightcorner}"]

		topwidth = self.countchars(output[0])
		
		for i in range(paddingY-2):
			output.append(border.left+(" "*(width))+border.right)



		for line in content:
			newline = f"{' '*paddingX} {line} {' '*paddingX}"

			mywidth = self.countchars(newline)

			if mywidth != topwidth:
				x = ((topwidth-mywidth)-2)
				if x % 2 == 0:
					zed = x // 2
					aed = zed
				else:
					zed = x // 2
					aed = x - zed
				newline = f"{' '*zed}{newline}{' '*aed}"

			output.append(f"{border.left}{newline}{border.right}")


		for i in range(paddingY-2):
			output.append(border.left+(" "*(width))+border.right)
		
		output.append(f"{border.bottomleftcorner}{border.bottom*(width)}{border.bottomrightcorner}")


		self.display(output, noblink, balanced=True)


	

	def nav_table(self, input_table, width=None, height=None, border=None, color="\033[7m"):
		"""Navigate a table and return selected table line"""

		# make sure input table is not empty

		if not input_table or len(input_table) == 0:
			exit("Nav Table: Input Table must not be empty")


		# store index, filter column index, reverse
		# and current dataset size

		index = 0

		filter_column = 0
		reverse = False

		dataset = [0, 10]

		last_footer = ""


		# begin main loop

		while True:

			# add instructions
			
			instructions = "\n(F - Filter  R - Reverse  E - Exit)"


			# make a copy of the input table
			
			display_table = copy.deepcopy(input_table)


			# remove header row
			
			header = display_table.pop(0)


			# add instructions for next and previous page

			if dataset[0] > 0:
				 instructions += " | <- Previous page"
			if dataset[1] < len(input_table)-1:
				instructions += " | Load More ->"


			# if filter add filter. Filter sorts by filter column
			# if the value is not a string. If the value is a string
			# filter sorts by the first char of the value in the filter
			# column

			if filter != None:
				display_table = sorted(display_table, key=lambda x:x[filter_column][0] if type(x[filter_column]) == str else x[filter_column], reverse=reverse)


			# cut table down to dataset size

			display_table = display_table[dataset[0]:dataset[1]]


			# highlight current selected row
				
			display_table[index][0] = color+display_table[index][0]
			display_table[index][-1] = str(display_table[index][-1])+"\033[0m"


			# add header row back in
			
			display_table.insert(0, header)


			# display table

			footer = (instructions+f"\nCurrent Filter: {header[filter_column] if filter_column != None else None} | Reverse: {reverse}").split("\n")

			if footer != last_footer:
				self.clear()
				last_footer = footer
			
			self.display_table(display_table, width=width, height=height, border=border, noblink=True, footer=footer)


			# get keypress from user

			key = getkey()


			# keys.UP, keys.DOWN, W, or S moves the index
			# of the selected row up or down respectively.

			# keys.RIGHT, keys.LEFT, D, and A increase or decrease
			# the dataset size (ie 10-20 instead of 0-10) respectively

			if key in keys.UP or key == "w":
				if index-1 >= 0:
					index -= 1
			elif key in keys.DOWN or key == "s":
				if index+1 < len(display_table)-1:
					index += 1

			elif key == keys.RIGHT or key == "d":
				if dataset[1] < len(input_table)-1:
					index = 0
					dataset[0] = dataset[1]
					if dataset[1]+10 < len(input_table)-1:
						dataset[1] += 10
					else:
						dataset[1] = len(input_table)-1
					self.clear()

			elif key == keys.LEFT or key == "a":
				if dataset[0] > 0:
					index = 0
					dataset[1] = dataset[0]
					if dataset[0]-10 > 0:
						dataset[0] -= 10
					else:
						dataset[0] = 0
					self.clear()


			# Space or Enter returns current selected row
					
			elif key == " " or key == "\n":
				return self.stripcolors(display_table[index+1])


			# R reverses filter

			elif key == "r":
				if reverse:
					reverse = False
				else:
					reverse = True


			# exit without selecting a row

			elif key == "e":
				return None


			# selects column to filter by. Defaults to column 0

			elif key == "f":
				prompts = []
				for i in input_table[0]:
					prompts.append([i, input_table[0].index(i)])
				filter_column = self.get_input("prompt", "Filter By", prompts=prompts)
				
				
	
	def display_table(self, input_table, width=None, height=None, border=None, noblink=False, footer=[], **kwargs):
		"""Display a table"""

		# update terminal size

		self.update_term_size()


		# convert input_table into a table of
		# strings

		table = []

		for row in input_table:
			table.append([str(item) for item in row])


		# Balance the table. ie: find the longest item
		# in each column and make all items in the column
		# that length

		columns = []

		for i in range(len(table[0])):
			columns.append(0)

		for row in table:
			for i in range(len(table[0])):
				length = self.countchars(row[i])
				if length > columns[i]:
					columns[i] = length


		# for row in table, find the max length
		# in the colum make each item that length

		output = []

		for row in table:
			new_row = []
			for index in range(len(row)):
				_len = columns[index]
				cell = row[index]
				padding = " "*((_len-self.countchars(cell))+3)
				new_row.append(cell+padding)

			output.append("".join(new_row))



		# if border add border

		if border:
			self.display_card(output, width, height, border, noblink=noblink, balanced=True)
		else:
			self.display(output, noblink=noblink, balanced=True)


		# Include footer here

		for line in footer:
			print(self.center(line, self.width))
			


	def get_input(self, _type, query_text="", border=None, width=None, height=None, align="center", **kwargs):
		"""Get input from user"""

		# I'm not even gunna try to comment what exactly this is
		# doing right now. Its a massive mess of if statements
		# the only cool stuff is if the datatype selected is "prompt"
		

		self.update_term_size()

		self.clear()

		if type(query_text) == str:
			question = query_text.split("\n")

			question.append("")
			question.insert(0, "")

		else:
			question = query_text

		if _type != "prompt":

			current = ""

			warning = ""

			cursor = "|          "

			while True:
				content = copy.deepcopy(question)
				content.append(f"=> {current}{cursor}\n{warning}")

				if border:
					self.display_card(content, width, height, border, True, True)
				else:
					self.display(content, True, True)

				warning = ""

				keypressed = getkey()

				if keypressed == "\n":
					if _type == "int" or _type == "float":
						valid = True
						try:
							if _type == "int":
								val = int(current)
							else:
								val = float(current)
						except:
							warning = f"Invalid {_type}"
							valid = False
							continue

						if "_min" in kwargs.keys():
							if val < kwargs["_min"]:
								warning = f"MIN Value is {kwargs['_min']}"
								valid = False
						if "_max" in kwargs.keys():
							if val > kwargs["_max"]:
								warning = f"MAX Value is {kwargs['_max']}"
								valid = False

						if valid:
							return val
					elif _type == "string":
						if "max_len" in kwargs.keys():
							if len(current) < kwargs["max_len"]:
								return current
							else:
								warning = f"Max Length for string is {kwargs['max_len']}"
						else:
							return current

				elif ord(keypressed) == 127:
					current = current[:-1]

				else:
					current += keypressed

		else:
			if "prompts" in kwargs.keys():
				raw_prompts = kwargs["prompts"]
			else:
				raise ScreenError("List of prompts must be included for type prompt")

			prompts = []
			return_values = []

			for i in raw_prompts:
				prompts.append(i[0])
				return_values.append(i[1])

			prompts = self.balance_strings(prompts, align=align)

			l1 = self.countchars(max(question, key=lambda x: self.countchars(x)))
			l2 = self.countchars(max(prompts, key=lambda x: self.countchars(x)))

			if l1 > l2:
				longest = l1
			else:
				longest = l2

			index = 0

			selector = kwargs["selector"] if "selector" in kwargs.keys() else ">"
			wipe = " "*self.countchars(selector)
			end = kwargs["end"] if "end" in kwargs.keys() else "  \033[0m"

			while True:
				q = copy.deepcopy(question)
				content = []
				for i in q:
					content.append(i)
					
				for i in prompts:
					if prompts.index(i) == index:
						content.append(f"{selector}  " + i + end)
					else:
						content.append(f"{wipe}  " + i + end)
						
				if border:
					self.display_card(content, width, height, border, noblink=True, balanced=False)
				else:
					self.display(content, noblink=True, balanced=False)

				key = getkey()

				new_index = index

				if key == keys.UP: new_index -= 1
				elif key == keys.DOWN: new_index += 1
				elif key == '\n': return return_values[index]

				if new_index >= 0 and new_index < len(prompts):
					index = new_index




	def onward(self, clear=True):
		"""Wait for input and move on"""
		self.move_cursor(self.height-1, 1)
		print("\033[7m<Enter>\033[0m")
		while True:
			key = getkey()
			if key == "\n" or key == " ":
				break
		if clear:
			self.clear()


	def exit(self):
		"""Just a handy exit function"""
		self.move_cursor(self.height, 1)
		self.show_cursor()


	def hide_cursor(self):
		"""Hide the Cursor"""
		if not self.cursor_hidden:
			self.cursor_hidden = True
			cursor.hide()

	def show_cursor(self):
		"""Show the cursor"""
		if self.cursor_hidden:
			self.cursor_hidden = False
			cursor.show()

	@staticmethod
	def clear():
		"""Clear Screen"""
		print("\033c", end="", flush=True)
		#os.system('cls' if os.name == 'nt' else 'clear')

	@staticmethod
	def refresh():
		"""Refresh Screen"""
		print("\033[H",end="")


	@staticmethod
	def move_cursor(y, x):
		print(f"\033[{y};{x}H", end="")


	@staticmethod
	def typewriter(string, pause=0.1, end="\n"):
		skip = False
		for char in string:
			sys.stdout.write(char)
			sys.stdout.flush()
			if ord(char) < 32 or ord(char) > 126:
				skip = True
			if char == "m" and skip:
				skip = False

			if not skip:
				time.sleep(pause)
				
		print("", end=end)

