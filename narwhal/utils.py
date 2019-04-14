import json

import docker
client = docker.from_env()

def add_proxy_network(name):
	containers = client.containers.list(filters={
		'label': 'service=narwhal-proxy'
	})
	network = client.networks.get(name)
	for container in containers:
		if container not in network.containers: network.connect(container)

def update_proxy_networks(container):
	image = container.image
	options = json.loads(image.labels.get('options', '{}'))
	if 'network' in options:
		add_proxy_network(options.get('network'))

def get_container(name):
	container = client.containers.get(name)
	assert container.name == name
	assert container.labels.get('service') == 'narwhal'
	return container

def get_containers():
	return client.containers.list(all=True, filters={
		'label': 'service=narwhal'
	})

def create_instance(repo, tag, options):
	image = client.images.pull(repo, tag=tag)
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
	containers = client.containers.list(all=True, filters={
		'ancestor': image.id
	})
	for container in containers:
		container.remove(force=True)
	prune_networks()
	client.images.remove(image.id)

def init_network(name):
	try:
		client.networks.get(name)
	except:
		client.networks.create(name, labels={
			'service': 'narwhal'
		})
	add_proxy_network(name)

def prune_networks():
	client.networks.prune(filters={
		'label': 'service=narwhal'
	})