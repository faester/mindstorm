import os

class TachoMotor:
	""" Abstraction of a motor in Mindstorms on EV3 """

	def __init__(self, basedir, motorNumber): 
		self.basedir = basedir
		self.motorNumber = motorNumber
		self.directory = os.path.join(basedir, "tacho-motor", f'motor{motorNumber}')
		self.commandsArray = self.commands()

	def __openFileInSubdir(self, filename, mode): 
		return open(os.path.join(self.directory, filename), mode)

	def commands(self): 
		commands = self.__openFileInSubdir("commands", "r")
		contents = commands.read().replace('\n', '')
		commands.close()
		print(contents.split(' '))
		return contents.split(' ')

	def sendCommand(self, command):
		commandFile = self.__openFileInSubdir("command", "w")
		commandFile.write(command)
		commandFile.close()
			
