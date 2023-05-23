import logging
from dataclasses import dataclass
from typing import Union

import torch
from get_models import MODEL_ID, TOKENIZER_ID
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          StoppingCriteria, StoppingCriteriaList)

from api.simple_ai.api.grpc.completion.server import LanguageModel

# tokenizer = AutoTokenizer.from_pretrained("StabilityAI/stablelm-base-alpha-3b")
# model = AutoModelForCausalLM.from_pretrained("StabilityAI/stablelm-base-alpha-3b")
# model.half().cuda()

# inputs = tokenizer("What's your mood today?", return_tensors="pt").to("cuda")
# tokens = model.generate(
#   **inputs,
#   max_new_tokens=64,
#   temperature=0.7,
#   do_sample=True,
# )
# print(tokenizer.decode(tokens[0], skip_special_tokens=True))

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [50278, 50279, 50277, 1, 0]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

# https://github.com/huggingface/transformers/issues/15799 might help us use multiple GPUs
@dataclass(unsafe_hash=True)
class StableLM(LanguageModel):
    try:
        tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)
    except Exception as ex:
        logging.exception(f"Could not load tokenizer: {ex}")
        tokenizer = None
    try:
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
        model.half().cuda()
    except Exception as ex:
        logging.exception(f"Could not load pretrained Peft model: {ex}")
        model = None
    


    def complete(
        self,
        prompt: str = "<|endoftext|>",
        suffix: str = "",
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        logprobs: int = 0,
        echo: bool = False,
        stop: Union[str, list] = "",
        presence_penalty: float = 0.0,
        frequence_penalty: float = 0.0,
        best_of: int = 0,
        logit_bias: dict = {},
    ) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

        tokens = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens, # probably adjust this
            temperature=temperature, # 
            do_sample=True,
            stopping_criteria=StoppingCriteriaList([StopOnTokens()])
        )
        print(self.tokenizer.decode(tokens[0], skip_special_tokens=True))
        return self.tokenizer.decode(tokens[0], skip_special_tokens=False)
