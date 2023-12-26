from extractors import (
    text_extract,
    summarize_context,
    function_extract,
)
from ui import print_sources, show_spinner
from data import ChatHistory, Parameter, Function, ChatType
from langchain.prompts import (
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain.schema.messages import (
    SystemMessage,
)

import os
from documents import format_docs
from api import chat_completion, prompt_completion
from config import get_config


class Chat:
    """
    Main handler for all chat tasks. Can respond to user messages
    as a chat assistant or query over docs/texts in the knowledge store
    """

    config = get_config()
    history = ChatHistory(max_length=config["runtime"]["max_history_size"])
    system_prompt = config["bot"]["system_prompt"]
    user_prompt_template = config["bot"]["user_prompt_template"]
    ai_prompt_template = config["bot"]["ai_prompt_template"]
    chat_type = config["bot"]["chat_type"]

    def __init__(self):
        self.user_message_prompt_template = (
            HumanMessagePromptTemplate.from_template(self.user_prompt_template)
        )
        self.ai_message_prompt_template = AIMessagePromptTemplate.from_template(
            self.ai_prompt_template
        )
        self.history.add_message(SystemMessage(content=self.system_prompt))

    def complete(self, prompt):
        with show_spinner():
            if self.history.is_too_long():
                self.__summarize_and_update_history()
            self.history.add_message(self.__get_human_message(content=prompt))
            response_text = self.__complete()
            self.history.add_message(
                self.__get_ai_message(content=response_text)
            )
            return response_text

    def __complete(self):
        if self.chat_type == ChatType.CHAT:
            return chat_completion(self.history)
        else:
            return prompt_completion(self.history.format())

    def __summarize_and_update_history(self):
        response_text = summarize_context(self.history, self.chat_type)
        system_prompt = (
            self.history.messages[0].content
            + f". Here is a summary of the conversation so far: {os.linesep}"
            + response_text
        )
        self.history = ChatHistory(
            max_length=self.config["runtime"]["max_history_size"]
        )
        self.history.add_messages(SystemMessage(content=system_prompt))

    def __over_text(self, query, text):
        with show_spinner("Extracting info..."):
            response = text_extract(query, text, self.chat_type)
        return response

    def __over_docs(self, query, docs, sources=False):
        print_sources(docs) if sources else None
        text = format_docs(docs)
        return self.__over_text(query, text=text)

    def over_db(self, db, query, sources=False):
        retriever = db.as_retriever()
        docs = retriever.invoke(query)
        response = self.__over_docs(query, docs=docs, sources=sources)
        self.history.add_messages(
            self.__get_human_message(content=query),
            self.__get_ai_message(content=response),
        )
        return response

    def over_function(self, query):
        # TODO: make this a configurable set of functions
        parameter = Parameter(
            "city_name", "string", "The name of the city, provided as a string"
        )
        function = Function(
            "get_weather",
            "Fetches the current temperature in Celsius at city provided",
            parameters=[parameter],
        )
        response = ""
        with show_spinner("Using functions..."):
            # response = function_extract(query, function)
            response = function_extract(query, function, self.chat_type)
        self.history.add_messages(
            self.__get_human_message(content=query),
            self.__get_ai_message(content=response),
        )
        return response

    def __get_human_message(self, content):
        return self.user_message_prompt_template.format(message=content)

    def __get_ai_message(self, content):
        return self.ai_message_prompt_template.format(message=content)
