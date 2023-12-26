from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from config import get_config

config = get_config()

OPENAI_API_BASE = config["bot"]["openai_api_base"]
OPENAI_API_KEY = config["bot"]["openai_api_key"]

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
    print(prompt)
    llm = OpenAI(openai_api_base=OPENAI_API_BASE, openai_api_key=OPENAI_API_KEY)
    try:
        return llm.invoke(prompt)
    except:
        raise InvalidApiResponseError
