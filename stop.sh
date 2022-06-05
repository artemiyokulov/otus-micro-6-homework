docker build -t otus-local-bootstraper -f infra/local/Dockerfile .
sudo docker run \
	  --network host \
	  --privileged \
	  -v /var/run/docker.sock:/var/run/docker.sock \
	  -v $(pwd):/app \
	  otus-local-bootstraper \
	  local-kube-delete-cluster