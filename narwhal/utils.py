import json

import docker
client = docker.from_env()

def get_container(name):
	container = client.containers.get(name)
	assert container.name == name
	assert container.labels.get('service') == 'narwhal'
	return container

def get_containers():
	return client.containers.list(all=True, filters={
		'label': 'service=narwhal'
	})

def create_instance(repo, tag):
	image = client.images.pull(repo, tag=tag)
	options = json.loads(image.labels.get('options', '{}'))
	options['detach'] = True
	options['labels'] = {
		'service': 'narwhal'
	}
	network = options.get('network')
	if network:
		init_network(network)
	return client.containers.create(image, **options)

def remove_instance(container):
	image = container.image
	containers = client.containers.list(filters={
		'ancestor': image.id
	})
	for container in containers:
		container.remove(force=True)
	prune_networks()
	client.images.remove(image.id, force=True)

def init_network(name):
	try:
		client.networks.get(name)
	except:
		client.networks.create(name, labels={
			'service': 'narwhal'
		})

def prune_networks():
	client.networks.prune(filters={
		'label': 'service=narwhal'
	})