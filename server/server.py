from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index(): 
	return 'Index!?'

@app.route('/test-template')
def testTemplate(): 
	return render_template('test.html', title = "Testing templates", greeting = "Hello Bandut")

