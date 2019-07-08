import os

from flask import Flask
from flask import render_template

def create_app(test_config = None): 
	# Create and configure the app
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(FOO = 'bar', GRINGOS = 'Loco')
	
	if test_config is None: 
		# Load config from py_file 
		app.config.from_pyfile('config.py', silent = True)
	else: 
		app.config.from_mapping(test_config)


	try: 
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import motor
	app.register_blueprint(motor.bp)

	@app.route('/hello')
	def hello(): 
		return 'We are up and running'


	@app.route('/test-template')
	def testTemplate(): 
		return render_template('test.html', title = "Testing templates", greeting = "Hello Bandut")

	return app
