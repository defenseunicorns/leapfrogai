ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder
USER root
ARG SDK_DEST=src/leapfrogai_sdk/build

WORKDIR /leapfrogai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

COPY --from=sdk /leapfrogai/${SDK_DEST} ${SDK_DEST}
COPY packages/whisper packages/whisper

RUN rm -f packages/whisper/build/*.whl
RUN python -m pip wheel "packages/whisper[dev]" -w packages/whisper/build --find-links=${SDK_DEST}

# download and covnert OpenAI's whisper base
ARG MODEL_NAME=openai/whisper-base
RUN pip install ctranslate2 transformers[torch] --no-index --find-links=packages/whisper/build/
RUN ct2-transformers-converter --model ${MODEL_NAME} --output_dir .model --copy_files tokenizer.json --quantization float32
RUN pip uninstall -y ctranslate2 transformers[torch]

RUN pip install packages/whisper/build/lfai_whisper*.whl --no-index --find-links=packages/whisper/build/

# Use hardened ffmpeg image to get compiled binaries
FROM cgr.dev/chainguard/ffmpeg:latest as ffmpeg

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11

ENV PATH="/leapfrogai/.venv/bin:$PATH"

WORKDIR /leapfrogai

COPY --from=ffmpeg /usr/bin/ffmpeg /usr/bin
COPY --from=ffmpeg /usr/bin/ffprobe /usr/bin
COPY --from=ffmpeg /usr/lib/lib* /usr/lib

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/
COPY --from=builder /leapfrogai/.model/ /leapfrogai/.model/

# set the path to the cuda 11.8 dependencies
ENV LD_LIBRARY_PATH \
/leapfrogai/.venv/lib64/python3.11/site-packages/nvidia/cublas/lib:\
/leapfrogai/.venv/lib64/python3.11/site-packages/nvidia/cudnn/lib

COPY packages/whisper/main.py .

EXPOSE 50051:50051

ENTRYPOINT ["python", "-u", "main.py"]
