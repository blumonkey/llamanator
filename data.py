from functools import reduce
from langchain.schema.messages import BaseMessage

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
