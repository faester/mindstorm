import flaskr.mindstorm.Mindstorm as Mindstorm 
from flask import Flask, request

class Motor:
	""" Abstraction of a motor in Mindstorms on EV3 """
	def __init__(self, basedir, motor_number = None, motor_name = None): 
		if motor_number is None and motor_name is None: 	
			self.mindstormDirectory = Mindstorm.Directory(basedir)
		elif motor_name is None:
			self.mindstormDirectory = Mindstorm.Directory(basedir, "tacho-motor", 'motor{motor_number}'.format(motor_number = motor_number))
		else:
			self.mindstormDirectory = Mindstorm.Directory(basedir, "tacho-motor", motor_name)
		self.motorIO = Mindstorm.SensorMotorIO(self.mindstormDirectory)
		self.__construct_metadata__()
		self.commands()
	
	def __construct_metadata__(self):
		self.motorIO.add_string_file('address', 'r')
		self.motorIO.add_int_file('speed', 'r')
		self.motorIO.add_int_file('speed_sp', 'rw')
		self.motorIO.add_array_file('command', 'w')
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
		self.motorIO.add_string_file('state', 'r')
		self.motorIO.add_string_file('stop_action', 'rw')
		self.motorIO.add_array_file('stop_actions', 'r')
		self.motorIO.add_dictionary_file('uevent', 'r')

	def commands(self): 
		d = self.get()
		result = d['commands']
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
		modified = self.motorIO.post(**kwargs)
		return {"Ok": True, "modified": modified}

class MotorList:
	""" Lists tacho motors """

	def __init__(self, basedir):
		self.mindstormDirectory = Mindstorm.Directory(basedir, 'tacho-motor')

	def get_motor_list(self):
		return {'motors': self.mindstormDirectory.get_subdirectories()}

	def get_directory_for_motor(self, motor_name):
		return self.mindstormDirectory.subdir(motor_name)
