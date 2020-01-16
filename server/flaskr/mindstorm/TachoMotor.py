import flaskr.mindstorm.Mindstorm as Mindstorm 

class Motor:
	""" Abstraction of a motor in Mindstorms on EV3 """

	def __init__(self, basedir, motorNumber): 
		self.mindstormDirectory = Mindstorm.Directory(basedir, "tacho-motor", f'motor{motorNumber}')
		self.commandsArray = self.commands()

	def commands(self): 
		return self.mindstormDirectory.read_from_file("commands").split(' ')

	def send_command(self, command):
		self.mindstormDirectory.write_to_file("command", command)

	def set_speed(self, speed): 
		self.mindstormDirectory.write_to_file("speed_sp", f'{speed}\n')

class MotorList:
	""" Lists tacho motors """

	def __init__(self, basedir):
		self.mindstormDirectory = Mindstorm.Directory(basedir, "tacho-motor")

	def get_motor_list():
		return self.mindstormDirectory.getSubdirectories()
