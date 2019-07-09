class TachoMotor:
	""" Abstraction of a motor in Mindstorms on EV3 """


	def __init__(self, basedir, motorNumber): 
		self.basedir = basedir
		self.motorNumber = motorNumber

	def commands(self): 
		return ["a","b","c"]		
