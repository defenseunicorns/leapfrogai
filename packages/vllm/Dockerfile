ARG ARCH=amd64

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 as builder

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN groupadd -g 65532 vglusers && \
    useradd -ms /bin/bash nonroot -u 65532 -g 65532 && \
    usermod -a -G video,sudo nonroot

WORKDIR /home/leapfrogai

# grab necesary python dependencies
RUN apt-get -y update \
    && apt-get -y install software-properties-common \
    && add-apt-repository universe \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get -y update


RUN apt-get -y install python3.11-full

# get deps for vllm compilation and model download
RUN chown -R nonroot /home/leapfrogai/
USER nonroot
RUN python3.11 -m venv .venv
ENV PATH="/home/leapfrogai/.venv/bin:$PATH"


# # create virtual environment for light-weight portability and minimal libraries
# # NOTE: We are copying to this filename because installing 'optional extras' from a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY build/*.whl build/
COPY build/leapfrogai_api*.whl leapfrogai_api-100.100.100-py3-none-any.whl
RUN pip install "leapfrogai_api-100.100.100-py3-none-any.whl[vllm]" --no-index --find-links=build/

# download model
ARG REPO_ID=TheBloke/Synthia-7B-v2.0-AWQ
ARG REVISION=main
ENV HF_HOME=/home/leapfrogai/.cache/huggingface
COPY scripts/model_download.py scripts/model_download.py

RUN REPO_ID=${REPO_ID} FILENAME=${FILENAME} REVISION=${REVISION} python3.11 scripts/model_download.py

ENV QUANTIZATION=awq

COPY main.py .
COPY config.yaml .

EXPOSE 50051:50051

ENTRYPOINT ["python3.11", "-m", "leapfrogai_api.types.cli", "--app-dir=.", "main:Model"]
