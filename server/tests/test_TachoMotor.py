import pytest

import flaskr
import flaskr.mindstorm.TachoMotor as TachoMotor
import os

def sys_class_path(): 
	return os.path.join('..', 'sys', 'class')

def __write_file(content, *path_components):
	f = open(os.path.join(sys_class_path(), *path_components), "w+")
	currentContent = f.read()
	if currentContent != content:
		f.write(content)
	f.close()

def __revert_sysclass_files():
	def write_motor0(file_name, content): 
		__write_file(content + '\n', "tacho-motor", "motor0", file_name)

	write_motor0('command', '# this file is write-only in the real FS')
	write_motor0('commands', 'run-forever run-to-abs-pos run-to-rel-pos run-timed run-direct stop reset')
	write_motor0('duty_cycle_sp', '0')
	write_motor0('position_sp', '0')
	write_motor0('ramp_down_sp', '0')
	write_motor0('ramp_up_sp', '0')
	write_motor0('speed_sp', '100')
	write_motor0('stop_action', 'coast')

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

def test_commands_with_full_path_ctor():
	subject = TachoMotor.Motor(os.path.join(sys_class_path(), "tacho-motor", "motor0"))
	actual = subject.commands()
	expected = ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
	assert all([a == b for a, b in zip(actual, expected)])
	assert len(actual) == len(expected), "number of elements differ"

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
	
def test_get():
	subject = TachoMotor.Motor(sys_class_path(), 0)
	expected = {}
	expected['address'] = 'ev3-ports:outA'
	expected['command'] = '# this file is write-only in the real FS'
	expected['commands'] = ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
	expected['count_per_rot'] = 360
	expected['driver_name'] = 'lego-ev3-l-motor'
	expected['duty_cycle'] = 0
	expected['duty_cycle_sp'] = 0
	expected['max_speed'] = 1050
	expected['polarity'] = 'normal'
	expected['position'] = 23638
	expected['position_sp'] = 0
	expected['ramp_down_sp'] = 0
	expected['ramp_up_sp'] = 0
	expected['speed'] = 0
	expected['speed_sp'] = 100
	expected['state'] = ''
	expected['stop_action'] = 'coast'
	expected['stop_actions'] = 'coast brake hold'
	expected['uevent'] = {'LEGO_DRIVER_NAME': 'lego-ev3-l-motor', 'LEGO_ADDRESS': 'ev3-ports:outA'}
	
	actual = subject.get()

	for k, v in expected.items(): 
		print (actual[k])
		assert v == actual[k]

def test_post_readonly_property(): 
	subject = TachoMotor.Motor(sys_class_path(), 0)
	expected = {'commands': ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']}
	
	subject.post(commands = 'this should not be written')

	actual = subject.get()
	
	assert actual['commands'] == expected['commands']
