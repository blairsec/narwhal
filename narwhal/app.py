import falcon
import os

from . import routes

SECRET = os.environ['NARWHAL_SECRET']

def build():
	auth = AuthMiddleware(SECRET)
	return start(auth)

def start(auth):
	api = falcon.API(middleware=auth)
	api.add_route('/instances', routes.Instances())
	api.add_route('/instances/{name}', routes.Instance())
	return api

class AuthMiddleware(object):

	def __init__(self, secret):
		self.secret = secret

	def process_resource(self, req, resp, resource, params):
		if not req.get_header('Authorization') == self.secret:
			raise falcon.HTTPUnauthorized()
