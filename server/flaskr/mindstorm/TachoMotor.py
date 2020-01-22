import flaskr.mindstorm.Mindstorm as Mindstorm 

class Motor:
	""" Abstraction of a motor in Mindstorms on EV3 """
	def __init__(self, basedir, motorNumber = None): 
		if motorNumber is None: 	
			self.mindstormDirectory = Mindstorm.Directory(basedir)
		else:
			self.mindstormDirectory = Mindstorm.Directory(basedir, "tacho-motor", f'motor{motorNumber}')
		self.__construct_metadata__()
		self.commands()
	
	def __construct_metadata__(self):
		def dosplit(x): return [item.replace('\n', '') for item in x.split(' ')]
		def str_no_newline(x): return x.replace('\n', '')
		def dictionary(x): 
			result={}
			for s in x.split('\n'):
				if '=' in s: 
					k, v = s.split('=')
					result[k] = v.replace('\n', '')
			return result
		self.readable_keys = ['address','command','commands','count_per_rot','driver_name','duty_cycle','duty_cycle_sp','max_speed','polarity','position','position_sp','ramp_down_sp','ramp_up_sp','speed','speed_sp','state','stop_action','stop_actions','uevent']
		self.writable_keys = ['command','duty_cycle_sp','position_sp','ramp_down_sp','ramp_up_sp','speed_sp','stop_action']
		self.mappers = {}
		self.mappers['address'] = str_no_newline
		self.mappers['command'] = str_no_newline
		self.mappers['commands'] = dosplit # Will fail if 'commands' are writeable
		self.mappers['count_per_rot'] = int
		self.mappers['driver_name'] = str_no_newline
		self.mappers['duty_cycle'] = int
		self.mappers['duty_cycle_sp'] = int
		self.mappers['max_speed'] = int
		self.mappers['polarity'] = str_no_newline
		self.mappers['position'] = int 
		self.mappers['position_sp'] = int 
		self.mappers['ramp_down_sp'] = int 
		self.mappers['ramp_up_sp'] = int 
		self.mappers['speed'] = int 
		self.mappers['speed_sp'] = int 
		self.mappers['state'] = str_no_newline
		self.mappers['stop_action'] = str_no_newline
		self.mappers['stop_actions'] = str_no_newline
		self.mappers['uevent'] = dictionary 

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
		self.mindstormDirectory.write_to_file('command', command)

	def get_speed(self, speed): 
		return self.get()['speed_sp']

	def set_speed(self, speed): 
		self.mindstormDirectory.write_to_file('speed_sp', f'{speed}\n')
	
	def get(self):
		result = {}
		for file_name in self.readable_keys:
			result[file_name] = self.mappers[file_name](self.mindstormDirectory.read_from_file(file_name))
		return result
	
	def post(self, **kwargs):
		for file_name in [f for f in self.writable_keys if f in kwargs]:
			self.mindstormDirectory.write_to_file(self.mappers[file_name](kwargs[file_name]))
		

class MotorList:
	""" Lists tacho motors """

	def __init__(self, basedir):
		self.mindstormDirectory = Mindstorm.Directory(basedir, 'tacho-motor')

	def get_motor_list(self):
		return {'motors': self.mindstormDirectory.get_subdirectories()}

	def get_directory_for_motor(self, motor_name):
		return self.mindstormDirectory.subdir(motor_name)
