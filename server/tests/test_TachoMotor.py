import pytest

import flaskr
import flaskr.mindstorm.TachoMotor as TachoMotor
import os

def sys_class_path(): 
	return os.path.join('..', 'sys', 'class')

def __write_file(subpath0, subpath1, filename, content):
	f = open(os.path.join(sys_class_path(), subpath0, subpath1, filename), "w+")
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
		subject = TachoMotor.Motor(sys_class_path(), 10)

def test_ctor_when_valid_motor():
	try:
		subject = TachoMotor.Motor(sys_class_path(), 0)
	except FileNotFoundError:
		pytest.fail('Did not expect an error opening motor0')

def test_commands():
	subject = TachoMotor.Motor(sys_class_path(), 0)
	actual = subject.commands()
	expected = ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
	assert all([a == b for a, b in zip(actual, expected)])
	assert len(actual) == len(expected), "number of elements differ"

def test_send_command():
	subject = TachoMotor.Motor(sys_class_path(), 0)
	subject.send_command("stop")

def test_set_speed():
	subject = TachoMotor.Motor(sys_class_path(), 0)
	subject.set_speed("100")
	
