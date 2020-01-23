import flaskr.mindstorm.Mindstorm as Mindstorm 

class Motor:
	""" Abstraction of a motor in Mindstorms on EV3 """
	def __init__(self, basedir, motorNumber = None): 
		if motorNumber is None: 	
			self.mindstormDirectory = Mindstorm.Directory(basedir)
		else:
			self.mindstormDirectory = Mindstorm.Directory(basedir, "tacho-motor", f'motor{motorNumber}')
		self.motorIO = Mindstorm.SensorMotorIO(self.mindstormDirectory)
		self.__construct_metadata__()
		self.commands()
	
	def __construct_metadata__(self):
		self.motorIO.add_string_file('address', 'r')
		self.motorIO.add_string_file('command', 'rw')
		self.motorIO.add_array_file('commands', 'r')
		self.motorIO.add_int_file('count_per_rot', 'r')
		self.motorIO.add_string_file('driver_name', 'r')
		self.motorIO.add_int_file('duty_cycle', 'r')
		self.motorIO.add_int_file('duty_cycle_sp', 'rw')
		self.motorIO.add_int_file('max_speed', 'r')
		self.motorIO.add_string_file('polarity', 'r')
		self.motorIO.add_int_file('position', 'r')
		self.motorIO.add_int_file('position_sp', 'rw')
		self.motorIO.add_int_file('ramp_down_sp', 'rw')
		self.motorIO.add_int_file('ramp_up_sp', 'rw')
		self.motorIO.add_int_file('speed', 'r')
		self.motorIO.add_int_file('speed_sp', 'rw')
		self.motorIO.add_string_file('state', 'r')
		self.motorIO.add_string_file('stop_action', 'rw')
		self.motorIO.add_string_file('stop_actions', 'r')
		self.motorIO.add_dictionary_file('uevent', 'r')

	def commands(self): 
		d = self.get()
		print(d)
		print(type(d))
		print(d['commands'])
		result = d['commands']
		print (result)
		print(type(result))
		return result

	def send_command(self, command):
		self.motorIO.post(command = command)

	def get_speed(self, speed): 
		return self.get()['speed_sp']

	def set_speed(self, speed): 
		self.motorIO.post(speed_sp =  speed)
	
	def get(self):
		return self.motorIO.get()
	
	def post(self, **kwargs):
		self.motorIO.post(**kwargs)

class MotorList:
	""" Lists tacho motors """

	def __init__(self, basedir):
		self.mindstormDirectory = Mindstorm.Directory(basedir, 'tacho-motor')

	def get_motor_list(self):
		return {'motors': self.mindstormDirectory.get_subdirectories()}

	def get_directory_for_motor(self, motor_name):
		return self.mindstormDirectory.subdir(motor_name)
