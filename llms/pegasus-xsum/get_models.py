import logging

TOKENIZER_ID = "google/pegasus-xsum"
MODEL_ID = "google/pegasus-xsum"

from transformers import PegasusForConditionalGeneration, PegasusTokenizer

if __name__ == "__main__":
    tokenizer = PegasusTokenizer.from_pretrained(TOKENIZER_ID)
    model = PegasusForConditionalGeneration.from_pretrained(MODEL_ID)