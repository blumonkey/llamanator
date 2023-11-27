from functools import reduce
from langchain.schema.messages import BaseMessage
import json

"""
Data Models
"""


class ChatHistory:
    """
    Helper class to keep track of the chat history
    """

    def __init__(self, max_length=200):
        self.messages = []
        self.max_length = max_length

    def add_message(self, chat_message: BaseMessage):
        self.messages.append(chat_message)

    def add_messages(self, *messages: BaseMessage):
        self.messages.extend(messages)

    def token_length(self):
        return reduce(
            (lambda total, curr: total + len(curr.content)),
            self.messages,
            0,
        )

    def is_too_long(self):
        return self.token_length() > self.max_length

    def get_messages(self):
        return self.messages


class Parameter:
    """
    Parameter for function, based on OpenAI functions
    https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools
    """

    def __init__(self, name, type, description):
        self.type = type
        self.name = name
        self.description = description


class Function:
    """
    Helper class to keep track of the chat history,
    based on OpenAI functions
    https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools
    """

    def __init__(self, name, description, parameters=[]):
        self.type = "function"
        self.name = name
        self.description = description
        self.parameters = parameters

    def get_json(self):
        parameters = {
            "type": "object",
            "properties": {},
            "required": [],
        }
        for p in self.parameters:
            parameters["properties"][p.name] = {
                "type": p.type,
                "description": p.description,
            }
            # TODO support configurable required parameters
            parameters["required"] = parameters["required"].append(p.name)

        func_dict = {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "parameters": parameters,
        }
        return json.dumps(func_dict)
