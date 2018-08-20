# narwhal

narwhal provides a web interface for managing Docker instances. Specifically, it is built to host CTF challenge servers. narwhal is built with [Falcon](https://falconframework.org/).

API documentation is available at https://blairsec.github.io/narwhal/.

## Registry
Creating a registry for narwhal follows the standard procedure. First, pull the `registry:2` image from Docker Hub.

Within the project directory, run:
```
λ touch docker-compose.yml
λ mkdir registry
λ mkdir auth
λ docker run --entrypoint htpasswd registry:2 -Bbn <user> <pass> > auth/htpasswd
```

Write to `docker-compose.yml`:
```yml
registry:
  restart: always
  image: registry:2
  ports:
    - 5000:5000
  environment:
    REGISTRY_AUTH: htpasswd
    REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
    REGISTRY_AUTH_HTPASSWD_REALM: registry
    REGISTRY_STORAGE_DELETE_ENABLED: "true"
  volumes:
    - ./registry:/var/lib/registry
    - ./auth:/auth
```

On the server where narwhal is running, authenticate the Docker client with the registry.

## Images
Since narwhal automates container creation, runtime flags must be provided in an image's label named `options`. They should be formatted as a JSON-encoded kwargs dictionary for the Docker Python SDK's [run method](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run).

Labels can be set within a Dockerfile:
```
LABEL options='{"ports": {"2222/tcp": 333}}'
```
narwhal will then expose port 2222 inside the container as port 3333 on the host. Note that the `detached` flag does not have to be provided.

An image corresponds to exactly one container. If more are necessary, consider using multiple tags that point to the same image.
