import os
import logging
import logging.config

from flask import Flask, send_from_directory
from flask import render_template
from . import pathbuilder
from .mindstorm import Device
import json 

def create_app(basedir = '/sys/class'): 
	# Create and configure the app
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(FOO = 'bar', GRINGOS = 'Loco')
	configure_logging()
	
	try: 
		os.makedirs(app.instance_path)
	except OSError as err:
		logging.info('Instance path "{instance_path}" already exists.'.format(instance_path = app.instance_path))
		pass

	logging.warn('base dir is {basedir}'.format(basedir = basedir))

	path_builder = pathbuilder.PathBuilder(app, basedir)

	@app.route('/hello')
	def hello(): 
		return 'We are up and running'

	@app.route('/mindstorm-client.js')
	def mindstorm_client():
		return send_from_directory('../static/', 'mindstorm-client.js')

	@app.route('/')
	def index():
		device_classes = Device.discover_basedir(basedir)
		# Build summary: for each class, list devices with name/address/driver
		summary = {}
		for class_name, dc in device_classes.items():
			devices = []
			for device_name in dc.get_devices():
				try:
					dev = dc.get_device(device_name)
					data = dev.get()
					devices.append({
						'name': device_name,
						'address': data.get('address', ''),
						'driver_name': data.get('driver_name', ''),
					})
				except Exception:
					devices.append({'name': device_name, 'address': '?', 'driver_name': '?'})
			summary[class_name] = devices
		return render_template('main.html', title = 'Mindstorm', heading = 'EV3 Device Explorer', device_classes = summary)

	return app


def configure_logging():
	logging.config.fileConfig('logging.config')
	logging.basicConfig(filename='../log/mindstorm.log',level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
	logging.debug('debug log example')
	logging.info('info log example')
	logging.warning('warning log example')
