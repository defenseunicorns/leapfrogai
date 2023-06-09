import logging
from dataclasses import dataclass

from get_models import TOKENIZER_ID, MODEL_ID
from simple_ai.api.grpc.completion.server import LanguageModel
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

@dataclass(unsafe_hash=True)
class PegasusXSum(LanguageModel):
    try:
        tokenizer = PegasusTokenizer.from_pretrained(TOKENIZER_ID)
    except Exception as ex:
        logging.exception(f"Could not load tokenizer: {ex}")
        tokenizer = None
    try:
        model = PegasusForConditionalGeneration.from_pretrained(MODEL_ID)
    except:
        logging(f"Could not load pretrained Pegasus model: {ex}")
        model = None

    def complete(
            self,
            prompt: str = "<|endoftext|>",
            max_tokens: int = 512
    ) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        tokens = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens
        )
        print(self.tokenizer.decode(tokens[0], skip_special_tokens=True))
        return self.tokenizer.decode(tokens[0], skip_special_tokens=False)