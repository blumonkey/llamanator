import os
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


"""
Handles API calls to the OPENAI API
"""


class InvalidApiResponseError(RuntimeError):
    pass


def chat_completion(history):
    chat = ChatOpenAI(
        openai_api_base=OPENAI_API_BASE, openai_api_key=OPENAI_API_KEY
    )
    messages = history.get_messages()
    response = chat.generate(messages=[messages])
    try:
        return response.generations[0][0].text
    except:
        raise InvalidApiResponseError


def prompt_completion(prompt):
    llm = OpenAI(openai_api_base=OPENAI_API_BASE, openai_api_key=OPENAI_API_KEY)
    try:
        return llm.invoke(prompt)
    except:
        raise InvalidApiResponseError
