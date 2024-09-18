ARG K3S_TAG=v1.28.8-k3s1
ARG CUDA_TAG=12.4.1-base-ubuntu22.04

FROM rancher/k3s:$K3S_TAG AS k3s

FROM nvidia/cuda:$CUDA_TAG

# Install the NVIDIA container toolkit
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
    apt-get update && \
    apt-get install -y nvidia-container-toolkit-base nvidia-container-toolkit nvidia-container-runtime util-linux && \
    nvidia-ctk runtime configure --runtime=containerd

COPY --from=k3s / / --exclude=/bin/
COPY --from=k3s /bin /bin

# Deploy the nvidia driver plugin on startup
COPY plugin/device-plugin-daemonset.yaml /var/lib/rancher/k3s/server/manifests/nvidia-device-plugin-daemonset.yaml

# Create the containerd configuration
RUN mkdir -p /etc/containerd/ && \
    echo '[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia]' > /etc/containerd/config.toml && \
    echo '  runtime_type = "io.containerd.runc.v2"' >> /etc/containerd/config.toml && \
    echo '  privileged_without_host_devices = false' >> /etc/containerd/config.toml && \
    echo '[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia.options]' >> /etc/containerd/config.toml && \
    echo '    BinaryName = "/usr/bin/nvidia-container-runtime"' >> /etc/containerd/config.toml



VOLUME /var/lib/kubelet
VOLUME /var/lib/rancher/k3s
VOLUME /var/lib/cni
VOLUME /var/log

# DIFF: resolve fsnotify issues
RUN sysctl -w fs.inotify.max_user_watches=100000 && \
    sysctl -w fs.inotify.max_user_instances=100000

ENV PATH="$PATH:/bin/aux"

ENTRYPOINT ["/bin/k3s"]
CMD ["agent"]
