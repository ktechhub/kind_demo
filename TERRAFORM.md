# Deploying Cluster with IaC

There is a folder called `terraform` which contains all the configurations to apply.

## Copy .env
```sh
cp .env.example .env
```

## Single command to kind on my ubuntu
```console
make setup-kind
```

## Initialize Terraform
```console
make terraform-init
```

## Plan Terraform
```console
make terraform-plan
```

## Apply Terraform
```console
make terraform-apply
```

## Destroy Cluster Setup
```console
make terraform-destroy
```


## Loadbalancer

**Check your address pool**
```console
docker network inspect -f '{{.IPAM.Config}}' kind
```
The output will contain a cidr such as `172.18.0.0/16`. We want our loadbalancer IP range to come from this subclass. We can configure metallb, for instance, to use `172.18.255.200` to `172.18.255.250` by creating the configmap.

Update the `manifest/metallb/configmap.yaml` with the address pool.

### Apply changes
Only apply if you have configmap ready.
```sh
make create-loadbalancer
```


### Example deployment and service with type loadbalancer plus ingress
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
---
kind: Service
apiVersion: v1
metadata:
  name: nginx-service
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  # Default port used by the image
  - port: 80
    targetPort: 80
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
  - host: test.botcraft.local
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: nginx-service
            port:
              number: 80
```

You can apply with:
```console
make demo-manifest-apply
```

### Get loadbalancer IP after applying service
```console
kubectl get svc/nginx-service -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Visit the loadbalancer ip to see your service running.

OR

Run:

```console
curl <lb-ip>
curl 172.18.255.200
```

### Using the hostname (Linux)
We’ll need to get the IP address of our kind node’s Docker container first by running:

Then add an entry to `/etc/hosts` with the IP address found that looks like:
```sh
172.18.255.200 test.botcraft.local
```

### Resolving hostname with Docker (All Machines)
The previous step work, but require working with the host system and are limited to Linux. We can instead create a Docker container. We can leverage docker run’s `--add-host` argument to add an entry to the container’s `/etc/hosts` file.
```console
docker run \
  --add-host test.botcraft.local:172.18.255.200 \
  --net kind \
  --rm \
  curlimages/curl:7.71.0 test.botcraft.local
```



## Running with terraform commands without using Makefile

```sh
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Update variable values

Run terraform commands
```sh
terraform init
terraform fmt
terraform validate
terraform apply
terraform destroy
```
