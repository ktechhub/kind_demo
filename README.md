# KinD -- Kubernetes in Docker

## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) (optional)
- [KIND](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

## Kind Installation

### Single command to kind on ubuntu
`for the ubuntu vms` --just run
```sh
make setup-kind
```

### Mac
```sh
brew install kind
```

### Windows
```sh
choco install kind
```

### ** Troubleshooting Port 80 problem
- If you are unable to create the cluster with the `kind-setup/config.yml` due to port 80 being in use. Check and kill the process running on it


- It could also be nginx running locally or you are running some webserver on your machine which operates on port 80.

### Help
```sh
kind --help
```

## Create Cluster
```sh
make kind-create-cluster
```

## Verify cluster is UP
```sh
kubectl cluster-info --context kind-demo-cluster
```

## Setup Nginx Ingress
```sh
make kind-ingress-setup
```

### check pods
```sh
kubectl -n ingress-nginx get pods
kubectl -n ingress-nginx get pods -w
```

## Setup Services Loadbalancer
**Check your address pool**
```sh
docker network inspect -f '{{.IPAM.Config}}' kind
```
The output will contain a cidr such as `172.18.0.0/16`. We want our loadbalancer IP range to come from this subclass. We can configure metallb, for instance, to use `172.18.255.200` to `172.18.255.250` by creating the configmap.

**Now apply the setup**

```sh
make create-loadbalancer
```

```sh
make lb-address-pool
```

### Test Loadbalancer or app deployments (optional)
Let's deploy nginx which has a service, deployment and an ingress. We will get the loadbalancer's IP and then test that in the browser or using any commandline utility like curl. You should see the default nginx page.

```sh
make demo-nginx-setup
```
**testing**
Visit the loadbalancer ip to see your service running.

OR

Run:
```sh
curl <lb-ip>
curl 172.18.255.200
```

### Using the hostname (Linux)
We’ll need to get the IP address of our kind node’s Docker container first by running:

```sh
kubectl get svc/nginx-service -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Then add an entry to `/etc/hosts` with the IP address found that looks like:
```sh
172.18.255.200 test.kalkulus.local
```

### Resolving hostname with Docker (All Machines)
The previous step work, but require working with the host system and are limited to Linux. We can instead create a Docker container. We can leverage docker run’s `--add-host` argument to add an entry to the container’s `/etc/hosts` file.
```sh
docker run \
  --add-host test.kalkulus.local:172.18.255.200 \
  --net kind \
  --rm \
  curlimages/curl:7.71.0 test.kalkulus.local
```

#### Port-forward a pod to check if it works
```sh
kubectl port-forward po/demo-fastapi-6678bbbd54-xbqnf :8000 -n backend
```

## Build Image
This builds the image and push it to the KinD cluster.
```sh
make image-build
```
## Deploy Kubernetes Manifests
```sh
make demo-fastapi-deploy-manifests
```

## Check deployment status
```sh
make demo-fastapi-status
```

## Destroy KinD Cluster
```sh
make kind-destroy-cluster
```