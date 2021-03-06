import flaskr.mindstorm.Mindstorm as Mindstorm

class SensorList:
	""" Lists sensors """

	def __init__(self, basedir):
		self.mindstormDirectory = Mindstorm.Directory(basedir, 'lego-sensor')

	def get_sensor_list(self):
		return {'sensors': self.mindstormDirectory.get_subdirectories()}

	def get_directory_for_sensor(self, sensor_name):
		return self.mindstormDirectory.subdir(sensor_name)

class Sensor:
	""" Abstraction of a sensor in Mindstorms on EV3 """
	def __init__(self, basedir, sensor_number = None, sensor_name = None): 
		if sensor_number is None and sensor_name is None: 	
			self.mindstormDirectory = Mindstorm.Directory(basedir)
		elif sensor_name is None:
			self.mindstormDirectory = Mindstorm.Directory(basedir, "lego-sensor", 'sensor{sensor_number}'.format(sensor_number = sensor_number))
		else:
			self.mindstormDirectory = Mindstorm.Directory(basedir, "lego-sensor", sensor_name)
		self.sensorIO = Mindstorm.SensorMotorIO(self.mindstormDirectory)
		self.__construct_metadata__()
	
	def __construct_metadata__(self):
		self.sensorIO.add_string_file('address', 'r')
		self.sensorIO.add_array_file('commands', 'r')
		self.sensorIO.add_int_file('decimals', 'r')
		self.sensorIO.add_string_file('driver_name', 'r')
		self.sensorIO.add_string_file('fw_version', 'r')
		self.sensorIO.add_string_file('mode', 'rw')
		self.sensorIO.add_array_file('modes', 'r')
		self.sensorIO.add_int_file('num_values', 'r')
		self.sensorIO.add_dictionary_file('uevent', 'r')
		self.sensorIO.add_string_file('units', 'r')
		for sensor_number in range(0,8): self.sensorIO.add_int_file('value{sensor_number}'.format(sensor_number = sensor_number), 'r')

	def get(self):
		return self.sensorIO.get()
	
	def post(self, **kwargs):		
		modified = self.sensorIO.post(**kwargs)
		return {"Ok": True, "modified": modified}

