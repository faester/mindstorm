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
		self.__import_external_modules__()

	@with_logging
	def __import_external_modules__(self): 
		motorList = TachoMotor.MotorList(self.basedir) 
		motors = [(motor, motorList.get_directory_for_motor(motor)) for motor in motorList.get_motor_list()['motors']]
		for motor in motors:
			self.logger.info(f'found motor {motor[0]} with dir {motor[1]}')
			tacho = TachoMotor.Motor(motor[1]) 
			logger = logging.getLogger('tacho-motor[0]')
			def post(): 
				data = request.data.decode('utf-8')
				logger.debug("received", data)
				body = json.loads(data)
				logger.info("deserialized completed")
				return tacho.post(**body)
			self.app.add_url_rule(rule = f'/motors/{motor[0]}', endpoint = f'motors/{motor[0]}-GET', view_func = tacho.get)
			self.app.add_url_rule(rule = f'/motors/{motor[0]}', endpoint = f'motors/{motor[0]}-POST', view_func = post, methods = ['POST'])
		self.app.add_url_rule(rule = '/motors', endpoint = 'motors', view_func = motorList.get_motor_list)
