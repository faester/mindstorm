import pytest

import flaskr
import flaskr.mindstorm.TachoMotor

def test_ctor():
	subject = flaskr.mindstorm.TachoMotor.TachoMotor("../../sys/class", 0)
	actual = subject.commands()
	expected = ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
	assert all([a == b for a, b in zip(actual, expected)])
	assert len(actual) == len(expected), "number of elements differ"
