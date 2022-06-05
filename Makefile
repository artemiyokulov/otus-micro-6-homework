# make>3.81 required for next statement to work properly
.ONESHELL:
SHELL = /bin/bash
#.SHELLFLAGS = -e

export REGISTRY_PORT = "5001"
export IMAGE_NAME = "otus-homework"
export IMAGE = "k3d-otus.localhost:$(REGISTRY_PORT)/$(IMAGE_NAME)"


local-helmfile-deps:
	@IMAGE=$(IMAGE) helmfile --file helm/helmfile.yaml deps

prepare-k3d:
	@k3d registry create otus.localhost -p $(REGISTRY_PORT)  || true
	@K3D_FIX_DNS=1 k3d cluster create otus \
	  --k3s-arg '--no-deploy=traefik@server:0' \
	  --registry-use k3d-otus.localhost:$(REGISTRY_PORT) \
	  -p "8080:80@loadbalancer" \
	  || true
	@k3d kubeconfig merge otus -d -u
	@kubectl config use-context k3d-otus
	@kubectl config set clusters.k3d-otus.server $$(kubectl config view -o jsonpath='{.clusters[?(@.name=="k3d-otus")].cluster.server}' | sed 's|host.docker.internal|localhost|g')

build-image:
	docker build -t 127.0.0.1:$(REGISTRY_PORT)/$(IMAGE_NAME) -f Dockerfile .
	docker push 127.0.0.1:$(REGISTRY_PORT)/$(IMAGE_NAME)

local-kube: prepare-k3d build-image local-helmfile-deps
	@kubectl config use-context k3d-otus
	IMAGE=$(IMAGE) helmfile --file helm/helmfile.yaml sync --set global.storageClass=local-path

local-helmfile-template:
	IMAGE=$(IMAGE) helmfile --file helm/helmfile.yaml template --set global.storageClass=local-path

local-kube-uninstall:
	@kubectl config use-context k3d-otus
	IMAGE=$(IMAGE) helmfile --file helm/helmfile.yaml destroy 

local-kube-reset: local-kube-uninstall local-kube

local-kube-delete-cluster:
	@k3d registry delete k3d-otus.localhost || true
	@k3d cluster delete otus || true