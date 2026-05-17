import pytest
import os

import flaskr.mindstorm.Device as Device

def sys_class_path():
	return os.path.join('..', 'example', 'sys', 'class')

def __write_file(content, *path_components):
	f = open(os.path.join(sys_class_path(), *path_components), "w+")
	currentContent = f.read()
	if currentContent != content:
		f.write(content)
	f.close()

def __revert_motor_files():
	def write_motor(file_name, content, motor_name):
		__write_file(content + '\n', "tacho-motor", motor_name, file_name)

	for motor_name in ['motor0', 'motor2']:
		write_motor('command', '', motor_name)
		write_motor('commands', 'run-forever run-to-abs-pos run-to-rel-pos run-timed run-direct stop reset', motor_name)
		write_motor('duty_cycle_sp', '0', motor_name)
		write_motor('position_sp', '0', motor_name)
		write_motor('ramp_down_sp', '0', motor_name)
		write_motor('ramp_up_sp', '0', motor_name)
		write_motor('speed_sp', '0', motor_name)
		write_motor('stop_action', 'coast', motor_name)

def __revert_sensor_files():
	def write_sensor(file_name, content, sensor_name):
		__write_file(content + '\n', "lego-sensor", sensor_name, file_name)

	write_sensor('mode', 'TOUCH', 'sensor0')
	write_sensor('num_values', '1', 'sensor0')

	write_sensor('mode', 'COL-REFLECT', 'sensor1')
	write_sensor('num_values', '1', 'sensor1')

	write_sensor('mode', 'IR-PROX', 'sensor2')
	write_sensor('num_values', '1', 'sensor2')

def setup_function():
	__revert_motor_files()
	__revert_sensor_files()

def teardown_function():
	__revert_motor_files()
	__revert_sensor_files()


# --- discover_basedir ---

def test_discover_basedir():
	classes = Device.discover_basedir(sys_class_path())
	assert 'tacho-motor' in classes
	assert 'lego-sensor' in classes

def test_discover_basedir_invalid_path():
	classes = Device.discover_basedir('/nonexistent/path')
	assert classes == {}


# --- DeviceClass ---

def test_device_class_lists_motors():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	devices = dc.get_devices()
	assert 'motor0' in devices
	assert 'motor1' in devices
	assert 'motor2' in devices

def test_device_class_lists_sensors():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	devices = dc.get_devices()
	assert 'sensor0' in devices
	assert 'sensor1' in devices
	assert 'sensor2' in devices


# --- Device (motor) ---

def test_motor_device_not_found():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	with pytest.raises(FileNotFoundError):
		dc.get_device('motor99')

def test_motor_get_address():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	data = device.get()
	assert data['address'] == 'ev3-ports:outA'

def test_motor_get_driver_name():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	data = device.get()
	assert data['driver_name'] == 'lego-ev3-l-motor'

def test_motor_get_int_attributes():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	data = device.get()
	assert data['count_per_rot'] == 360
	assert data['max_speed'] == 1050
	assert isinstance(data['speed'], int)

def test_motor_get_commands_array():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	data = device.get()
	expected = ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
	assert data['commands'] == expected

def test_motor_get_stop_actions_array():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	data = device.get()
	assert data['stop_actions'] == ['coast', 'brake', 'hold']

def test_motor_get_uevent_dict():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	data = device.get()
	assert data['uevent'] == {'LEGO_DRIVER_NAME': 'lego-ev3-l-motor', 'LEGO_ADDRESS': 'ev3-ports:outA'}

def test_motor_writable_keys():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	data = device.get()
	writable = data['__writable']
	# command and stop_action should be writable (singular of pair)
	assert 'command' in writable
	assert 'stop_action' in writable
	# commands and stop_actions should NOT be writable (plural)
	assert 'commands' not in writable
	assert 'stop_actions' not in writable

def test_motor_command_paired_with_commands():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	attr = device.attributes['command']
	assert attr.paired_with == 'commands'

def test_motor_post_readonly_ignored():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	before = device.get()['commands']
	device.post(commands='this should not be written')
	after = device.get()['commands']
	assert before == after

def test_motor_post_command():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	device.post(command='run-forever')
	data = device.get()
	assert data['command'] == 'run-forever'

def test_motor_post_speed_sp():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	device.post(speed_sp=42)
	data = device.get()
	assert data['speed_sp'] == 42

def test_motor_post_stop_action():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	device.post(stop_action='brake')
	data = device.get()
	assert data['stop_action'] == 'brake'

def test_motor_post_list_flattens():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	device.post(speed_sp=[123, 456])
	data = device.get()
	assert data['speed_sp'] == 123

def test_motor_post_returns_modified():
	dc = Device.DeviceClass(sys_class_path(), 'tacho-motor')
	device = dc.get_device('motor0')
	modified = device.post(speed_sp=50, command='stop')
	assert 'speed_sp' in modified
	assert 'command' in modified


# --- Device (sensor) ---

def test_sensor_get_address():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor0')
	data = device.get()
	assert data['address'] == 'ev3-ports:in2'

def test_sensor_get_driver_name():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor0')
	data = device.get()
	assert data['driver_name'] == 'lego-ev3-touch'

def test_sensor_num_values_gating():
	"""Only value0 should be present for sensor0 (num_values=1)."""
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor0')
	data = device.get()
	assert data['num_values'] == 1
	assert 'value0' in data
	assert 'value1' not in data
	assert 'value7' not in data

def test_sensor_mode_paired_with_modes():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor1')
	attr = device.attributes['mode']
	assert attr.paired_with == 'modes'
	assert attr.writable is True

def test_sensor_modes_readonly():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor1')
	attr = device.attributes['modes']
	assert attr.writable is False

def test_sensor_color_modes():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor1')
	data = device.get()
	assert data['modes'] == ['COL-REFLECT', 'COL-AMBIENT', 'COL-COLOR', 'REF-RAW', 'RGB-RAW', 'COL-CAL']

def test_sensor_post_mode():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor1')
	device.post(mode='RGB-RAW')
	data = device.get()
	assert data['mode'] == 'RGB-RAW'

def test_sensor_post_mode_returns_modified():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor1')
	modified = device.post(mode='COL-AMBIENT')
	assert 'mode' in modified

def test_sensor_ir_modes():
	dc = Device.DeviceClass(sys_class_path(), 'lego-sensor')
	device = dc.get_device('sensor2')
	data = device.get()
	assert data['modes'] == ['IR-PROX', 'IR-SEEK', 'IR-REMOTE', 'IR-REM-A', 'IR-S-ALT', 'IR-CAL']
	assert data['mode'] == 'IR-PROX'
