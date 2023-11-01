from functools import reduce
import os

"""
Data Models
"""


class ChatMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content
        self.content_length = len(content.split())

    def get_wire_format(self):
        return {"role": self.role, "content": f"{self.content}"}

    def get_content_length(self):
        return self.content_length

    def get_simple_format(self):
        return f"{self.role}: {self.content}"


class ChatHistory:
    def __init__(self, max_length=200):
        self.messages = []
        self.max_length = max_length

    def add_message(self, chat_message: ChatMessage):
        self.messages.append(chat_message)

    def add_messages(self, *messages: ChatMessage):
        self.messages.extend(messages)

    def token_length(self):
        return reduce(
            (lambda total, curr: total + curr.get_content_length()),
            self.messages,
            0,
        )

    def is_too_long(self):
        return self.token_length() > self.max_length

    def get_wire_format(self):
        return list(map(lambda x: x.get_wire_format(), self.messages))

    def get_simple_format(self):
        return f"{os.linesep}".join(
            list(map(lambda x: x.get_simple_format(), self.messages))
        )
