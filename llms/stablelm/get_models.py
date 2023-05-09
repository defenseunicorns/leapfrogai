import logging

# TOKENIZER_ID = "stabilityai/stablelm-tuned-alpha-7b"
TOKENIZER_ID = "stabilityai/stablelm-tuned-alpha-3b"
# TOKENIZER_ID="mosaicml/mpt-1b-redpajama-200b-dolly"
# TOKENIZER_ID = "StabilityAI/stablelm-tuned-alpha-7b"
MODEL_ID = "stabilityai/stablelm-tuned-alpha-3b"
REDPANDA_ID= "mosaicml/mpt-1b-redpajama-200b-dolly"

# import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, StoppingCriteria, StoppingCriteriaList
import time
import numpy as np
from torch.nn import functional as F
import os
from threading import Thread

if __name__ == "__main__":
    from huggingface_hub import snapshot_download, hf_hub_download
    
    # print(f"Starting to load the model to memory")
    # m = AutoModelForCausalLM.from_pretrained(
    #     "stabilityai/stablelm-tuned-alpha-7b", torch_dtype=torch.float16).cuda()
    # tok = AutoTokenizer.from_pretrained("stabilityai/stablelm-tuned-alpha-7b")
    for repo_id in (TOKENIZER_ID):
        try:
            print(f"Downloading model { repo_id}")
            # hf_hub_download(repo_id=repo_id)
            snapshot_download(repo_id)
        except Exception as ex:
            logging.exception(f"Could not retrieve {repo_id}: {ex}")
