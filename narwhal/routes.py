import json

import falcon

from . import utils

def load_stream(req):
	try:
		return json.loads(str(req.stream.read().decode("utf-8")))
	except:
		raise falcon.HTTPBadRequest('Bad request', 'Invalid JSON data.')

def get_metadata(container):
	return {
		'image': container.image.tags[0],
		'status': container.status,
		'labels': container.labels,
	}

class Instances(object):

	def on_get(self, req, resp):
		response = {}
		containers = utils.get_containers()
		for container in containers:
			response[container.name] = get_metadata(container)
		resp.body = json.dumps(response, indent=2)

	def on_post(self, req, resp):
		data = load_stream(req)
		repo = data.get('repo')
		tag = data.get('tag')
		environment = data.get('environment', {})
		try:
			resp.body = utils.create_instance(repo, tag, environment).name
		except Exception as e:
			raise falcon.HTTPInternalServerError('Internal server error', str(e))

class Instance(object):

	def get_container(self, name):
		try:
			return utils.get_container(name)
		except:
			raise falcon.HTTPBadRequest('Bad request', 'Invalid name.')

	def on_get(self, req, resp, name):
		container = self.get_container(name)
		response = get_metadata(container)
		resp.body = json.dumps(response, indent=2)

	def on_patch(self, req, resp, name):
		data = load_stream(req)
		container = self.get_container(name)
		self.handle_action(container, data.get('action'))

	def on_delete(self, req, resp, name):
		container = self.get_container(name)
		utils.remove_instance(container)

	def handle_action(self, container, action):
		utils.update_proxy_networks(container)
		if action == 'start':
			container.start()
		elif action == 'stop':
			container.stop()
		elif action == 'restart':
			container.restart()