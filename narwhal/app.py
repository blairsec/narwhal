import falcon

from . import routes

def start():
	api = falcon.API()
	api.add_route('/instances', routes.Instances())
	api.add_route('/instances/{name}', routes.Instance())
	return api
