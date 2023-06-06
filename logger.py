
with open("log.txt", "w") as file:
	file.write("")

def log(string):
	with open("log.txt", "a+") as file:
		file.write(string+"\n")
