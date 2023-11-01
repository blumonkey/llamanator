import openai
import os

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_base = OPENAI_API_BASE
openai.api_key = OPENAI_API_KEY

"""
Handles API calls to the OPENAI API
"""


def chat_completion(
    history, model=OPENAI_API_KEY, temperature=0.6, max_tokens=1900
):
    response = openai.ChatCompletion.create(
        model=model,
        messages=history.get_wire_format(),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()  # type: ignore
