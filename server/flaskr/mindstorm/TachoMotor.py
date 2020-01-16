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

	def __readFromSubdir(self, filename):
		f = self.__openFileInSubdir(filename, "r")
		content = f.read().replace('\n', '')
		f.close()
		return content

	def __writeToSubdir(self, filename, content):
		f = self.__openFileInSubdir(filename, "w")
		f.write(content)
		f.close()
		

	def commands(self): 
		return self.__readFromSubdir("commands").split(' ')

	def sendCommand(self, command):
		self.__writeToSubdir("command", command)

	def setSpeed(self, speed): 
		commandFile = self.__writeToSubdir("speed_sp", f'{speed}\n')
