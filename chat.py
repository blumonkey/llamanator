from extractors import text_extract, summarize_context, function_extract
from ui import print_sources, show_spinner
from data import ChatHistory, Parameter, Function
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import os
from documents import format_docs
from api import chat_completion

"""
Main handler for all chat tasks. Can respond to user messages 
as a chat assistant or query over docs/texts in the knowledge store
"""


class Chat:
    history = ChatHistory(max_length=100)

    def __init__(self, system_prompt):
        self.history.add_message(SystemMessage(content=system_prompt))

    def complete(self, prompt):
        with show_spinner():
            if self.history.is_too_long():
                self.__summarize_and_update_history()
            self.history.add_message(HumanMessage(content=prompt))
            response_text = chat_completion(self.history)
            self.history.add_message(AIMessage(content=response_text))
            return response_text

    def __summarize_and_update_history(self):
        response_text = summarize_context(self.history)
        system_prompt = (
            self.history.messages[0].content
            + f". Here is a summary of the conversation so far: {os.linesep}"
            + response_text
        )
        self.history = ChatHistory(max_length=1900)
        self.history.add_messages(
            SystemMessage(content=system_prompt),
        )

    def __over_text(self, query, text):
        with show_spinner("Extracting info..."):
            response = text_extract(query, text)
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
            HumanMessage(content=query),
            AIMessage(content=response),
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
            response = function_extract(query, function)
        self.history.add_messages(
            HumanMessage(content=query),
            AIMessage(content=response),
        )
        return response
