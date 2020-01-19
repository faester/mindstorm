import os
import logging
import logging.config

from flask import Flask
from flask import render_template
from . import motor
from . import pathbuilder

def create_app(test_config = None): 
	# Create and configure the app
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(FOO = 'bar', GRINGOS = 'Loco')
	configure_logging()
	
	if test_config is None: 
		# Load config from py_file 
		app.config.from_pyfile('config.py', silent = True)
	else: 
		app.config.from_mapping(test_config)


	try: 
		os.makedirs(app.instance_path)
	except OSError as err:
		logging.info(f'Instance path "{app.instance_path}" already exists.')
		pass


	builder = pathbuilder.PathBuilder(app)


	@app.route('/hello')
	def hello(): 
		return 'We are up and running'


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
