# Deploy a registry server

Before you can deploy a registry, you need to install Docker on the host. A registry is an instance of the `registry` image, and runs within Docker.

## Run a local registry

```console
docker run -d -p 5000:5000 --restart=always --name registry registry
```

### Adding addr
```console
docker run -d \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5001 \
  -p 5001:5001 \
  --name registry-test \
  registry:2
```

### Using certs
```console
docker run -d \
  --restart=always \
  --name registry \
  -v "$(pwd)"/certs:/certs \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -p 443:443 \
  registry:2
```

### Restricting access
Using basic auth with tls
[https://docs.docker.com/registry/deploying/#restricting-access](https://docs.docker.com/registry/deploying/#restricting-access)

```console
docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  -v "$(pwd)"/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -v "$(pwd)"/certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  registry:2
```
Try to pull an image from the registry, or push an image to the registry. These commands fail.
Log in to the registry.

```console
docker login myregistrydomain.com:5000
```

## Deploy with Composefile
```yaml
registry:
  restart: always
  image: registry:2
  ports:
    - 5000:5000
  environment:
    REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
    REGISTRY_HTTP_TLS_KEY: /certs/domain.key
    REGISTRY_AUTH: htpasswd
    REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
    REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
  volumes:
    - /path/data:/var/lib/registry
    - /path/certs:/certs
    - /path/auth:/auth
```

```console
docker-compose up -d
```

## Build Image
```console
docker build -t test:v0 .
```

## Tag Image for registry
```sh
docker tag test:v0 localhost:5000/test:v0
```

## Push Image
```sh
docker push localhost:5000/test:v0
```

## Remove images
```sh
docker image rm test:v0
docker image rm localhost:5000/test:v0
```

## Pull from local registry
```sh
docker pull localhost:5000/test:v0
```