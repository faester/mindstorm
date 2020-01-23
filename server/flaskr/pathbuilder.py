import logging
import flaskr.mindstorm.TachoMotor as TachoMotor
from flask import jsonify, request
import json

def with_logging(func):
	""" A little wrapper experiment. Not directly useful :) """
	def logit(*args, **kwargs):
		log = logging.getLogger(func.__name__)
		log.debug("Running " + func.__name__)	
		try:
			result = func(*args, **kwargs)
			log.debug("Completed " + func.__name__)	
		except Exception as ex:
			log.warning("Exception running " + func.__name__, ex)
			raise ex
	return logit

class PathBuilder:
	@with_logging
	def __init__(self, app, basedir):
		self.logger = logging.getLogger('PathBuilder')
		self.app = app
		self.logger.debug('initialized') 
		self.basedir = basedir
		self.__setup_routes__()

	def __setup_routes__(self): 
		@self.app.route('/motors')
		def motors():
			motorList = TachoMotor.MotorList(self.basedir) 
			return motorList.get_motor_list()

		@self.app.route('/motors/<motor_name>')
		def get_motor(motor_name):
			motor = TachoMotor.Motor(self.basedir, motor_name = motor_name)
			return motor.get()

		@self.app.route('/motors/<motor_name>', methods = ['POST'])
		def post_motor(motor_name):
			motor = TachoMotor.Motor(self.basedir, motor_name = motor_name)
			body = json.loads(request.data.decode('utf-8'))
			return motor.post(**body)
