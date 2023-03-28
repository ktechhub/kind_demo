include .env
export $(shell sed 's/=.*//' .env)

export TAG=0.0.1

setup-kind:
	curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
	chmod +x ./kind
	sudo mv ./kind /usr/local/bin
	which kind
	kind version

# Terraform Specific
terraform-init:
	cd terraform && \
	terraform init && \
	cd ..


terraform-plan:
	cd terraform && \
	terraform fmt && \
	terraform validate && \
	terraform plan && \
	cd ..

terraform-apply:
	cd terraform && \
	terraform apply -auto-approve && \
	kind get clusters && \
	kubectl config get-contexts && \
	kubectl cluster-info --context kind-bot-kind && \
	cd ..

terraform-destroy:
	cd terraform && \
	terraform destroy -auto-approve && \
	cd ..


# KIND CLI Specific
kind-create-cluster:
	cd kind-setup && \
	kind create cluster --config config.yaml && \
	kind get clusters && \
	kubectl config get-contexts && \
	kubectl cluster-info --context kind-demo-cluster && \
	cd ..

kind-ingress-setup:
	kubectl apply -f setup-manifests/ingress-nginx/setup.yaml

	kubectl wait --namespace ingress-nginx \
	--for=condition=ready pod \
	--selector=app.kubernetes.io/component=controller \
	--timeout=90s

kind-destroy-cluster:
	kind delete cluster --name demo-cluster


## For All (Will be updated later)
create-loadbalancer:
	printf "\nApplying Setup Manifest File...\n"
	kubectl apply -f setup-manifests/metallb/metallb.yaml
	kubectl wait --namespace metallb-system \
	--for=condition=ready pod \
	--selector=app=metallb \
	--timeout=90s

lb-address-pool:
	printf "\nApplying Config...\n"
	kubectl apply -f setup-manifests/metallb/address_pool.yaml

demo-nginx-setup:
	kubectl apply -f setup-manifests/demo/deploy.yaml
	printf "\nWaiting for pods to be ready...\n"
	sleep 60
	kubectl get svc/nginx-service -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'

image-build:
	printf "\nDone Building demo-fastapi:latest...\n"
	docker build -t demo-fastapi:latest demo_fastapi/.

	printf "\nPushing demo-fastapi:latest to kind cluster...\n"
	kind load docker-image demo-fastapi:latest --name demo-cluster

	printf "\nDisplaying all images...\n"
	docker images | grep latest


demo-fastapi-deploy-manifests:
	printf "\nApplying all namespaces...\n"
	kubectl apply -f manifests/namespace.yaml

	printf "\nAppling dashboard manifests...\n"
	kubectl apply -f manifests/deployment.yaml
	kubectl apply -f manifests/service.yaml
	kubectl apply -f manifests/ingress.yaml

demo-fastapi-status:
	printf "\nWaiting for deployment to be ready...\n"
	kubectl wait deployment -n backend demo-fastapi --for condition=Available=True --timeout=2s
	printf "\nGetting all...\n"
	kubectl get all -n backend
	printf "\nGetting loadbalancer ip... You should see the index page of the dashboard\n"
	kubectl get svc/demo-fastapi-service -o=jsonpath='{.status.loadBalancer.ingress[0].ip}' -n backend | xargs
	printf "\nDashboard IP --->>> 172.18.255.200\n"
	curl 172.18.255.200
	printf "\nIngress check for demo-fastapi -- demo-fastapi.kalkulus.local\n"
	docker run \
	--add-host demo-fastapi.kalkulus.local:172.18.255.200 \
	--net kind \
	--rm \
	curlimages/curl:7.71.0 demo-fastapi.kalkulus.local