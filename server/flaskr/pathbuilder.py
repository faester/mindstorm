import logging
import flaskr.mindstorm.TachoMotor as TachoMotor


class PathBuilder:
	def __init__(self, app, basedir):
		self.logger = logging.getLogger('PathBuilder')
		self.app = app
		self.logger.debug('initialized') 
		self.basedir = basedir
		self.__import_external_modules__()

	def __import_external_modules__(self): 
		self.app.add_url_rule(rule = '/pt0', endpoint = '/pt0', view_func = pt0.answer )
		self.app.add_url_rule(rule = '/pt1', endpoint = '/pt1', view_func = pt1.answer )

		motorList = TachoMotor.MotorList(self.basedir) 
		motors = [(motor, motorList.get_directory_for_motor(motor)) for motor in motorList.get_motor_list()]
		for motor in motors:
			self.logger.info(f'found motor {motor[0]} with dir {motor[1]}')
			tacho = TachoMotor.Motor(motor[1]) 
			self.app.add_url_rule(rule = f'/motors/{motor[0]}/commands', endpoint = f'motors/{motor[0]}/commands', view_func = tacho.commands)
		self.app.add_url_rule(rule = '/motors', endpoint = 'motors', view_func = motorList.get_motor_list)
