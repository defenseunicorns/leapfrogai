from openai.types.beta.threads.text_content_block_param import TextContentBlockParam
from pydantic import TypeAdapter

"""Validators that can be used to verify the types of OpenAI classes that inherit from TypedDict"""

TextContentBlockParamValidator = TypeAdapter(TextContentBlockParam)
