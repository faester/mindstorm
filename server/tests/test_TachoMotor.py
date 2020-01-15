import pytest

import flaskr
import flaskr.mindstorm.TachoMotor
import os

def motorPath(): 
	return os.path.join('..', 'sys', 'class')

def setup_function():
	print("Prior to running test!!!")

def teardown_function():
	print("after")

def test_ctor_when_invalid_motor():
	with pytest.raises(FileNotFoundError) as exception:
		subject = flaskr.mindstorm.TachoMotor.TachoMotor(motorPath(), 10)

def test_ctor_when_valid_motor():
	try:
		subject = flaskr.mindstorm.TachoMotor.TachoMotor(motorPath(), 0)
	except FileNotFoundError:
		pytest.fail('Did not expect an error opening motor0')

def test_commands():
	subject = flaskr.mindstorm.TachoMotor.TachoMotor(motorPath(), 0)
	actual = subject.commands()
	expected = ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
	assert all([a == b for a, b in zip(actual, expected)])
	assert len(actual) == len(expected), "number of elements differ"

def test_sendCommand():
	subject = flaskr.mindstorm.TachoMotor.TachoMotor(motorPath(), 0)
	subject.sendCommand("stop")
