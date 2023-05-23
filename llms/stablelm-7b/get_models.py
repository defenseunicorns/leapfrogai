from transformers import AutoModelForCausalLM, AutoTokenizer

TOKENIZER_ID = "stabilityai/stablelm-tuned-alpha-7b"
MODEL_ID = "stabilityai/stablelm-tuned-alpha-7b"


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
