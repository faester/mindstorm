import pytest

import flaskr
import flaskr.mindstorm.TachoMotor

def test_ctor():
	subject = flaskr.mindstorm.TachoMotor.TachoMotor("../../sys/class", 0)
	actual = subject.commands()
	assert all([a == b for a, b in zip(actual, ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset'])])

	
