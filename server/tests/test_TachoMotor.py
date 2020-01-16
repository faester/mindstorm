import pytest

import flaskr
import flaskr.mindstorm.TachoMotor
import os

def sysClassPath(): 
	return os.path.join('..', 'sys', 'class')

def __write_file(subpath0, subpath1, filename, content):
	f = open(os.path.join(sysClassPath(), subpath0, subpath1, filename), "w+")
	currentContent = f.read()
	if currentContent != content:
		f.write(content)
	f.close()

def __revert_sysclass_files():
	__write_file("tacho-motor", "motor0", "command", "# this file is write-only in the real FS\n")
	__write_file("tacho-motor", "motor0", "commands", "run-forever run-to-abs-pos run-to-rel-pos run-timed run-direct stop reset\n")

def setup_function():
	__revert_sysclass_files()

def teardown_function():
	__revert_sysclass_files()

def test_ctor_when_invalid_motor():
	with pytest.raises(FileNotFoundError) as exception:
		subject = flaskr.mindstorm.TachoMotor.TachoMotor(sysClassPath(), 10)

def test_ctor_when_valid_motor():
	try:
		subject = flaskr.mindstorm.TachoMotor.TachoMotor(sysClassPath(), 0)
	except FileNotFoundError:
		pytest.fail('Did not expect an error opening motor0')

def test_commands():
	subject = flaskr.mindstorm.TachoMotor.TachoMotor(sysClassPath(), 0)
	actual = subject.commands()
	expected = ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
	assert all([a == b for a, b in zip(actual, expected)])
	assert len(actual) == len(expected), "number of elements differ"

def test_sendCommand():
	subject = flaskr.mindstorm.TachoMotor.TachoMotor(sysClassPath(), 0)
	subject.sendCommand("stop")

def test_setSpeed():
	subject = flaskr.mindstorm.TachoMotor.TachoMotor(sysClassPath(), 0)
	subject.setSpeed("100")
	
