from api import chat_completion
from data import ChatHistory
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import os

"""
Methods that perform specific tasks using the chat API, 
such as summarization or text extraction.
"""


def summarize_context(history):
    summarize_context_history = ChatHistory()
    summarize_context_history.add_messages(
        SystemMessage(
            content="Your sole purpose is to express the topic of conversation in as few words as possible. The conversation is as follows: ",
        ),
        *history.messages[1:],
        HumanMessage(
            content="Summarize the topic of above conversation in as few words as possible.",
        ),
    )

    return chat_completion(summarize_context_history)


def text_extract(query, text):
    """Extract points relevant to a query from text."""

    history = ChatHistory()
    history.add_messages(
        SystemMessage(
            content="You are a helpful assistant who follows instructions carefully.",
        ),
        HumanMessage(
            content=f"""Query: {query}

            Please concisely rewrite the following text, extracting the points 
            most interesting, pertinent and important to the preceding query. 
            Don't invent information. If there is no relevant information,
            be silent.
            
            Text: {text}""",
        ),
    )
    return chat_completion(history)
