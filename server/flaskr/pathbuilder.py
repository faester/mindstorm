import logging
import flaskr.mindstorm.TachoMotor as TachoMotor
from flask import jsonify, request, render_template
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

class Decoder: 
	def __init__(self):
		self.log = logging.getLogger('decode')

	def decode(self, req):
		self.log.info('is decoding')
		contentType = req.headers.get('Content-Type')
		self.log.info(contentType)
		if contentType == 'application/x-www-form-urlencoded': 
			self.log.info('form encoding')
			return req.form
		return req.json
	
class Encoder: 
	def __init__(self):
		self.log = logging.getLogger('Encoder')

	def encode(self, req, template_name, response_data):
		acceptHeader = req.headers.get('Accept')
		if 'text/html' in acceptHeader.split(','):
			self.log.debug(f'Got "{acceptHeader}" accept reader. Trying the template {template_name}')
			return render_template(template_name, **response_data)
		self.log.debug(f'Got "{acceptHeader}" accept reader. Returning response data.')
		return response_data


class PathBuilder:
	@with_logging
	def __init__(self, app, basedir):
		self.logger = logging.getLogger('PathBuilder')
		self.app = app
		self.logger.debug('initialized') 
		self.basedir = basedir
		self.decoder = Decoder()
		self.encoder = Encoder()
		self.__setup_routes__()

	def __setup_routes__(self): 

		@self.app.route('/motors')
		def motors():
			motorList = TachoMotor.MotorList(self.basedir) 
			return self.encoder.encode(request, 'motors.html', {"motors": motorList.get_motor_list()})

		@self.app.route('/motors/<motor_name>')
		def get_motor(motor_name):
			motor = TachoMotor.Motor(self.basedir, motor_name = motor_name)
			return self.encoder.encode(request, 'motor.html', motor.get())

		@self.app.route('/motors/<motor_name>', methods = ['POST'])
		def post_motor(motor_name):
			motor = TachoMotor.Motor(self.basedir, motor_name = motor_name)
			body = self.decoder.decode(request)
			motor.post(**body)
			return self.encoder.encode(request, 'motor.html', motor.get())
