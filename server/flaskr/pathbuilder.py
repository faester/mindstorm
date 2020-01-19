import logging
from . import motor


class PathBuilder:
	def __init__(self, app):
		self.logger = logging.getLogger('PathBuilder')
		self.app = app
		self.logger.debug('initialized') 
		self.__import_external_modules__()

	def __import_external_modules__(self): 
		self.app.register_blueprint(motor.motor, url_prefix='/motors')
		self.app.register_blueprint(motor.motor, url_prefix='/motors0')
		pt0 = PathTest(0)
		pt1 = PathTest(1)

		self.app.add_url_rule(rule = '/pt0', endpoint = '/pt0', view_func = pt0.answer )
		self.app.add_url_rule(rule = '/pt1', endpoint = '/pt1', view_func = pt1.answer )


class PathTest: 
	def __init__(self, number): 
		self.number = number
	
	def answer(self):
		return str(self.number)
