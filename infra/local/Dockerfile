FROM debian:11-slim

WORKDIR /app

COPY --from=quay.io/roboll/helmfile:v0.144.0 /usr/local/bin/helmfile /usr/local/bin/helmfile

RUN \
    apt update && \
    apt install -y make curl && \
    rm -rf /var/lib/apt/lists/* && \curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
    chmod 700 get_helm.sh && \
    ./get_helm.sh && \
    chmod +x /usr/local/bin/helmfile && \
    curl -sSL https://get.docker.com/ | sh && \
    curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    mv kubectl /usr/local/bin/kubectl && chmod +x /usr/local/bin/kubectl

ENTRYPOINT ["make"]