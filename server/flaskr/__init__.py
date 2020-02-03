import os
import logging
import logging.config

from flask import Flask, send_from_directory
from flask import render_template
from . import pathbuilder
import json 

def create_app(basedir = '../sys/class'): 
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

	@app.route('/sensor-template')
	def motor_template():
		return send_from_directory('../static', 'sensor-template.html')

	@app.route('/motor-template')
	def sensor_template():
		return send_from_directory('../static', 'motor-template.html')

	@app.route('/')
	def index():
		return render_template('main.html', title = 'main page', heading = 'We are trying to be dynamic')

	@app.route('/test-template')
	def testTemplate(): 
		return render_template('test.html', title = "Testing templates", greeting = "Hello Bandut")

	return app


def configure_logging():
	logging.config.fileConfig('logging.config')
	logging.basicConfig(filename='../log/mindstorm.log',level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
	logging.debug('debug log example')
	logging.info('info log example')
	logging.warning('warning log example')
