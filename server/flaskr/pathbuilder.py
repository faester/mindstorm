import logging
import flaskr.mindstorm.Device as Device
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
		contentType = req.headers.get('Content-Type')
		self.log.debug(contentType)
		if contentType == 'application/x-www-form-urlencoded': 
			self.log.debug('form encoding')
			return req.form
		self.log.debug('json encoding')
		return req.json
	
class Encoder: 
	def __init__(self):
		self.log = logging.getLogger('Encoder')

	def encode(self, req, template_name, response_data):
		acceptHeader = req.headers.get('Accept')
		if 'text/html' in acceptHeader.split(','):
			self.log.debug('Got "{acceptHeader}" accept reader. Trying the template {template_name}'.format(acceptHeader = acceptHeader, template_name = template_name))
			response_data['main_model'] = response_data
			return render_template(template_name, **response_data)
		self.log.debug('Got "{acceptHeader}" accept reader. Returning response data.'.format(acceptHeader = acceptHeader))
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
		@self.app.route('/<class_name>')
		def device_list(class_name):
			device_class = Device.DeviceClass(self.basedir, class_name)
			devices = device_class.get_devices()
			data = {'class_name': class_name, 'devices': devices}
			return self.encoder.encode(request, 'device_list.html', data)

		@self.app.route('/<class_name>/<device_name>')
		def get_device(class_name, device_name):
			device_class = Device.DeviceClass(self.basedir, class_name)
			device = device_class.get_device(device_name)
			data = device.get()
			data['class_name'] = class_name
			data['device_name'] = device_name
			data['__attributes'] = {name: {'type': attr.attr_type, 'paired_with': attr.paired_with} for name, attr in device.attributes.items()}
			return self.encoder.encode(request, 'device.html', data)

		@self.app.route('/<class_name>/<device_name>', methods = ['POST'])
		def post_device(class_name, device_name):
			device_class = Device.DeviceClass(self.basedir, class_name)
			device = device_class.get_device(device_name)
			body = self.decoder.decode(request)
			device.post(**body)
			return get_device(class_name, device_name)
