import os

class MindstormDirectory:
	""" Defines methods for communicating with a mindstorm directory """

	def __init__(self, base, *args):
		self.directory = os.path.join(base, *args)
	
	def __openFileInSubdir(self, filename, mode): 
		return open(os.path.join(self.directory, filename), mode)

	def readFromFile(self, filename):
		f = self.__openFileInSubdir(filename, "r")
		content = f.read().replace('\n', '')
		f.close()
		return content

	def writeToFile(self, filename, content):
		f = self.__openFileInSubdir(filename, "w")
		f.write(content)
		f.close()	

