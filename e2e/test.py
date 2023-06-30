import openai

openai.api_base = "http://localhost:8080/openai"
openai.api_key = "removed"

prompt = """<|im_start|>system
You are an AI assistant that answers participates in chat discussions in an honest, concise, friendly way.<|im_end|>
<|im_start|>user
Write two sequences composed of 3 'A's and 2 'B's such that there are no two successive identical letter. Be consice.<|im_end|>
<|im_assistant|>
"""

# prompt = """
# <|im_start|>system
# You are an AI assistant that follows instruction extremely well. Your role is to accept some input and summarize it. For example:

# User: Summarize the main idea in the following text:
# The rapid growth of technology has led to significant advancements in various industries. From communication and transportation to healthcare and education, technology has played a crucial role in improving our lives. However, we must also be cautious of the potential negative effects, such as job loss due to automation and privacy concerns.

# Assistant: Technology's rapid growth has positively impacted various industries but also raises concerns about job loss and privacy.
# <|im_end|>
# <|im_start|>user
# Summarize the main idea in the following text:
# Few-shot prompting is a technique used to guide large language models (LLMs), like GPT-3, towards generating desired outputs by providing them with a few examples of input-output pairs. While few-shot prompting has shown promising results, there are limitations to this approach. This method allows for in-context learning by conditioning the model using examples, guiding it to produce better responses.<|im_end|><|im_assistant|>
# """

response = openai.Completion.create(
    # model="text-davinci-003",
    model="ctransformers",
    prompt=prompt,
    max_tokens=700,
    temperature=0.3,
    stream=True,  # this time, we set stream=True,
)

for event in response:
    print(event.choices[0].text, end="", flush=True)
print("\n")