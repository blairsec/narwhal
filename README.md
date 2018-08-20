# narwhal

narwhal provides a web interface for managing Docker instances. Specifically, it is built to host CTF challenge servers. narwhal is built with [Falcon](https://falconframework.org/).

API documentation is available at https://blairsec.github.io/narwhal/.

## Registry
narwhal obtains images by pulling from registries. The server should be pre-authenticated with the registry it is using.

## Images
Since narwhal automates container creation, runtime flags must be provided in an image's label named `options`. They should be formatted as a JSON-encoded kwargs dictionary from the Docker Python SDK's [method](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run). The `detached` flag does not have to be provided.

An image will correspond to exactly one  container. If more are necessary, consider using multiple tags that point to the same image.
