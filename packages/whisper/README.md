# LeapfrogAI Whisper Backend

A LeapfrogAI API-compatible [whisper](https://huggingface.co/openai/whisper-base) wrapper for audio transcription inferencing across CPU & GPU infrastructures.


# Usage

## Zarf Package Deployment

To build and deploy just the whisper Zarf package (from the root of the repository):

> Deploy a [UDS cluster](/README.md#uds) if one isn't deployed already

```shell
make build-whisper LOCAL_VERSION=dev
uds zarf package deploy packages/whisper/zarf-package-whisper-*-dev.tar.zst --confirm
```

## Local Development

To run the vllm backend locally without K8s (starting from the root directory of the repository):

```shell
python -m pip install src/leapfrogai_sdk
cd packages/whisper
python -m pip install ".[dev]"
ct2-transformers-converter --model openai/whisper-base --output_dir .model --copy_files tokenizer.json --quantization float32
python -u main.py
```
