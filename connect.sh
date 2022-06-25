#!/bin/sh
k3d kubeconfig merge otus -d -u
kubectl config use-context k3d-otus
kubectl config set clusters.k3d-otus.server $(kubectl config view -o jsonpath='{.clusters[?(@.name=="k3d-otus")].cluster.server}' | sed 's|host.docker.internal|localhost|g')