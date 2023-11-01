from extractors import text_extract, summarize_context
from ui import print_sources, show_spinner
from data import ChatHistory, ChatMessage
import os
from document import format_docs, similarity
from api import chat_completion

"""
Main handler for all chat tasks. Can respond to user messages 
as a chat assistant or query over docs/texts in the knowledge store

TODO: Make this a class?
"""

history = ChatHistory(max_length=100)


def init_chat(system_prompt):
    history.add_message(ChatMessage(role="system", content=system_prompt))


def complete(prompt):
    global history
    with show_spinner():
        if history.is_too_long():
            summarize_and_update_history()
        history.add_message(ChatMessage(role="user", content=prompt))
        response_text = chat_completion(history)
        history.add_message(
            ChatMessage(role="assistant", content=response_text)
        )
        return response_text


def summarize_and_update_history():
    global history
    response_text = summarize_context(history)
    system_prompt = (
        history.messages[0].content
        + f". Here is a summary of the conversation so far: {os.linesep}"
        + response_text
    )
    history = ChatHistory(max_length=1900)
    history.add_messages(
        ChatMessage(role="system", content=system_prompt),
    )


def over_text(query, text):
    with show_spinner("Extracting info..."):
        response = text_extract(query, text)
    return response


def over_docs(query, docs, sources=False):
    print_sources(docs) if sources else None
    text = format_docs(docs)
    return over_text(query, text=text)


def over_db(db, query, sources=False):
    global history
    docs = similarity(db, query, k=3)
    response = over_docs(query, docs=docs, sources=sources)
    history.add_messages(
        ChatMessage(
            role="user",
            content=query,
        ),
        ChatMessage(
            role="assistant",
            content=response,
        ),
    )
    return response
