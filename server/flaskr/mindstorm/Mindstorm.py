import os

class Directory:
	""" Defines methods for communicating with a mindstorm directory """

	def __init__(self, base, *args):
		self.directory = os.path.join(base, *args)
	
	def __openFileInSubdir(self, filename, mode): 
		return open(os.path.join(self.directory, filename), mode)

	def read_from_file(self, filename):
		f = self.__openFileInSubdir(filename, "r")
		content = f.read()
		f.close()
		return content

	def write_to_file(self, filename, content):
		f = self.__openFileInSubdir(filename, "w")
		f.write(content)
		f.close()	

	def get_subdirectories(self):
		return [name for name in os.listdir(self.directory)
			if os.path.isdir(os.path.join(self.directory, name))]

	def subdir(self, subdir):
		return os.path.join(self.directory, subdir)

class SensorMotorIO:
	""" Performs conversions and mappings to/from mindstorm dir """
	def __init__(self, mindstormDirectory):
		self.mindstormDirectory = mindstormDirectory
		self.readable_keys = []
		self.writable_keys = []
		self.mappers = {}
		def dosplit(x): return [item.replace('\n', '') for item in x.split(' ')]
		def str_no_newline(x): return x.replace('\n', '')
		def dictionary(x): 
			result={}
			for s in x.split('\n'):
				if '=' in s: 
					k, v = s.split('=')
					result[k] = v.replace('\n', '')
			return result
		self.__split__ = dosplit
		self.__str__ = str_no_newline
		self.__dictionary__ = dictionary

	def __add_key__(self, key, mode):
		if 'w' in mode: self.writable_keys.append(key)
		if 'r' in mode: self.readable_keys.append(key)

	def add_int_file(self, file_name, mode):
		self.mappers[file_name] = int
		self.__add_key__(file_name, mode)

	def add_string_file(self, file_name, mode):
		self.mappers[file_name] = self.__str__
		self.__add_key__(file_name, mode)

	def add_dictionary_file(self, file_name, mode):
		self.mappers[file_name] = self.__dictionary__
		self.__add_key__(file_name, mode)

	def add_array_file(self, file_name, mode):
		self.mappers[file_name] = self.__split__
		self.__add_key__(file_name, mode)
	
	def get(self):
		result = {}
		for file_name in self.readable_keys:
			result[file_name] = self.mappers[file_name](self.mindstormDirectory.read_from_file(file_name))
		return result
	
	def post(self, **kwargs):
		modified = []
		for file_name in [f for f in self.writable_keys if f in kwargs]:
			modified.append(file_name)
			print (file_name, kwargs[file_name])
			self.mindstormDirectory.write_to_file(file_name, str(kwargs[file_name]))
		return modified

