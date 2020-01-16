import os

class Directory:
	""" Defines methods for communicating with a mindstorm directory """

	def __init__(self, base, *args):
		self.directory = os.path.join(base, *args)
	
	def __openFileInSubdir(self, filename, mode): 
		return open(os.path.join(self.directory, filename), mode)

	def read_from_file(self, filename):
		f = self.__openFileInSubdir(filename, "r")
		content = f.read().replace('\n', '')
		f.close()
		return content

	def write_to_file(self, filename, content):
		f = self.__openFileInSubdir(filename, "w")
		f.write(content)
		f.close()	

	def get_subdirectories():
		return [name for name in os.listdir(self.directory)
			if os.path.isdir(os.path.join(self.directory, name))]
