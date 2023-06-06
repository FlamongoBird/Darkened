"""


 ██████  ██    ██  █████   ██████ ██   ██ ██████   █████  ███████ ███████ 
██    ██ ██    ██ ██   ██ ██      ██  ██  ██   ██ ██   ██ ██      ██      
██    ██ ██    ██ ███████ ██      █████   ██████  ███████ ███████ ███████ 
██ ▄▄ ██ ██    ██ ██   ██ ██      ██  ██  ██      ██   ██      ██      ██ 
 ██████   ██████  ██   ██  ██████ ██   ██ ██      ██   ██ ███████ ███████ 
    ▀▀                                                                    
                                                                          

The m͟o͟s͟t͟ ͟s͟e͟c͟u͟r͟e͟ password application to ever exist.
QuackPass is the very cutting edge of secureness. It uses a unique
combination of simple hashing and plain text passwords to protect
your passwords from any malicous parties. 


Made by @InvisibleOne and @JankyCoder, originally for use with
our glorious Avocado package.
"""





import hashlib
import os
import json

try:
	from replit import db
except:
	print("Mode `replit` unavailable")


class LoginManager():
	def __init__(self, salt="amonguspenis", mode="txt", file="passwords.txt"):
		"""Salt -> Salt value | mode -> 'txt' or 'replit' | file -> file to store passwords in (only for 'txt' mode)"""

		self.salt = salt
		self.mode = mode
		self.file = file

		if self.mode == "txt":
			self.db = TxtDB(file)
		else:
			self.db = ReplitDB()

	def hash(self, value):
		"""Hash a value"""
		return hashlib.sha256(f"{value}{self.salt}".encode()).hexdigest()

	def add_user(self, username, password):
		"""Add a user"""
		data = self.db.get_data()

		passphrase = self.hash(password)
		userphrase = self.hash(username)

		if userphrase in data['usernames']:
			return "username taken"
		else:
			data['usernames'].append(userphrase)
			data['full_data'].append(passphrase+userphrase)
			self.db.store_data(data)
			return "success"


	def check(self, username, password):
		"""Check if a username and password are valid"""
		data = self.db.get_data()
		passphrase = self.hash(password)
		userphrase = self.hash(username)

		if username not in data['usernames']:
			return "user does not exist"

		else:
			if passphrase+userphrase in data['full_data']:
				return True
			else:
				return "incorrect password"


	def login(self, username_prompt="Username: ", password_prompt="Password: "):
		data = self.db.get_data()
		logged_in = False
		while not logged_in:
			username = input(username_prompt)
			if self.hash(username) in data['usernames']:
				password = input(password_prompt)
				if self.check(username, password):
					return username
				else:
					print("Incorrect Password")
			else:
				print(f"Username {username} does not exist!")

	




class TxtDB():
	def __init__(self, file):
		self.file = file

		if not os.path.isfile(self.file):
			os.system(f"touch {self.file}")
			
			with open(self.file, "w") as file:
				file.write(json.dumps({"full_data":[], "usernames": []}))

	def get_data(self):
		with open(self.file, "r") as file:
			return json.loads(file.read())

	def store_data(self, data):
		with open(self.file, "w") as file:
			file.write(json.dumps(data))


class ReplitDB():
	def __init__(self):
		keys = db.keys()
		if "passwords" not in keys:
			db["passwords"] = {"full_data":[], "usernames":[]}

	def get_data(self):
		return db['passwords']


	def store_data(self, data):
		db['passwords'] = data
	

