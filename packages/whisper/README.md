# LeapfrogAI Whisper Backend

A LeapfrogAI API-compatible [whisper](https://huggingface.co/openai/whisper-base) wrapper for audio transcription inferencing across CPU & GPU infrastructures.


# Usage

To run the vllm backend locally (starting from the root directory of the repository):

```shell
python -m pip install src/leapfrogai_sdk
cd packages/whisper
python -m pip install ".[dev]"
ct2-transformers-converter --model openai/whisper-base --output_dir .model --copy_files tokenizer.json --quantization float32
python -u main.py
```
