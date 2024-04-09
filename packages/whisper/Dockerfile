FROM --platform=$BUILDPLATFORM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev as builder

WORKDIR /leapfrogai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

# download and covnert OpenAI's whisper base
ARG MODEL_NAME=openai/whisper-base
RUN pip install transformers[torch]
RUN pip install ctranslate2
RUN ct2-transformers-converter --model ${MODEL_NAME} --output_dir .model --copy_files tokenizer.json --quantization float32

COPY build/*.whl build/
COPY build/leapfrogai_api*.whl leapfrogai_api-100.100.100-py3-none-any.whl

RUN pip install leapfrogai_api-100.100.100-py3-none-any.whl[whisper] --no-index --find-links=build/

# Use hardened ffmpeg image to get compiled binaries
FROM cgr.dev/chainguard/ffmpeg:latest as ffmpeg

# hardened and slim python image
FROM --platform=$BUILDPLATFORM ghcr.io/defenseunicorns/leapfrogai/python:3.11

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

COPY main.py .

EXPOSE 50051:50051

ENTRYPOINT ["python", "-u", "main.py"]
