import flaskr.mindstorm.Mindstorm as Mindstorm 

class Motor:
	""" Abstraction of a motor in Mindstorms on EV3 """

	def __init__(self, basedir, motorNumber): 
		self.mindstormDirectory = Mindstorm.Directory(basedir, "tacho-motor", f'motor{motorNumber}')
		self.commandsArray = self.commands()

	def commands(self): 
		return self.mindstormDirectory.readFromFile("commands").split(' ')

	def sendCommand(self, command):
		self.mindstormDirectory.writeToFile("command", command)

	def setSpeed(self, speed): 
		self.mindstormDirectory.writeToFile("speed_sp", f'{speed}\n')
