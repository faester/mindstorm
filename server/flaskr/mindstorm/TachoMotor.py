import flaskr.mindstorm.MindstormDirectory as MindstormDirectory

class TachoMotor:
	""" Abstraction of a motor in Mindstorms on EV3 """

	def __init__(self, basedir, motorNumber): 
		self.mindstormDirectory = MindstormDirectory.MindstormDirectory(basedir, "tacho-motor", f'motor{motorNumber}')
		self.commandsArray = self.commands()

	def commands(self): 
		return self.mindstormDirectory.readFromFile("commands").split(' ')

	def sendCommand(self, command):
		self.mindstormDirectory.writeToFile("command", command)

	def setSpeed(self, speed): 
		self.mindstormDirectory.writeToFile("speed_sp", f'{speed}\n')
