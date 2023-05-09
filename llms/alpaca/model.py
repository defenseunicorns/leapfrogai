import logging
from dataclasses import dataclass
from typing import Union

from get_models import ALPACA_ID, LLAMA_ID, TOKENIZER_ID
from peft import PeftModel
from simple_ai.api.grpc.completion.server import LanguageModel
from transformers import GenerationConfig, LLaMAForCausalLM, LLaMATokenizer
import torch
# https://github.com/huggingface/transformers/issues/15799 might help us use multiple GPUs
@dataclass(unsafe_hash=True)
class AlpacaModel(LanguageModel):
    try:
        tokenizer = LLaMATokenizer.from_pretrained(TOKENIZER_ID)
    except Exception as ex:
        logging.exception(f"Could not load tokenizer: {ex}")
        tokenizer = None
    try:
        model = LLaMAForCausalLM.from_pretrained(
            LLAMA_ID,
            load_in_8bit=True,
            device_map="auto",
        )
    except Exception as ex:
        logging.exception(f"Could not load pretrained LlaMa model: {ex}")
        model = None
    try:
        model = PeftModel.from_pretrained(model, ALPACA_ID)
    except Exception as ex:
        logging.exception(f"Could not load pretrained Peft model: {ex}")
        model = None

    def complete(
        self,
        prompt: str = "<|endoftext|>",
        suffix: str = "",
        max_tokens: int = 512,
        temperature: float = 1.0,
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
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            num_beams=4,
        )

        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        # input_ids = inputs["input_ids"]
        # input_ids = input_ids.cuda()

        tokens = model.generate(
            **inputs,
            max_new_tokens=64,
            temperature=0.7,
            do_sample=True,
            stopping_criteria=StoppingCriteriaList([StopOnTokens()])
        )
        print(tokenizer.decode(tokens[0], skip_special_tokens=True))

        

        output = self.model.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=max_tokens,
        )
        print(f"Output: {output}")
        results = []
        for sequence in output.sequences:
            results.append(self.tokenizer.decode(sequence))
        # define your PyTorch model here
        # release unused memory caches held by PyTorch
        torch.cuda.empty_cache()
            # print(f"Sequence: {sequence}")
            # results.append(self.tokenizer.decode(sequence).split("### Response:")[1].strip())
        return results[0]
