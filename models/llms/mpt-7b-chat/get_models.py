MODEL_ID = "mosaicml/mpt-7b-chat"
from transformers import AutoModelForCausalLM, AutoTokenizer

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True)