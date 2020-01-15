import os

class TachoMotor:
	""" Abstraction of a motor in Mindstorms on EV3 """

	def __init__(self, basedir, motorNumber): 
		self.basedir = basedir
		self.motorNumber = motorNumber
		self.directory = os.path.join(basedir, "tacho-motor", f'motor{motorNumber}')
		self.commandsArray = self.commands()

	def commands(self): 
		commands = open(os.path.join(self.directory, "commands"), "r")
		contents = commands.read().replace('\n', '')
		commands.close()
		print(contents.split(' '))
		return contents.split(' ')
