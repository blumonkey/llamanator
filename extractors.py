from api import chat_completion
from data import ChatHistory, ChatMessage

"""
Methods that perform specific tasks using the chat API, 
such as summarization or text extraction.
"""


def summarize_context(history):
    summarize_context_history = ChatHistory()
    summarize_context_history.add_messages(
        ChatMessage(
            role="system",
            content="Your sole purpose is to express the topic of conversation in as few words as possible. The conversation is as follows: ",
        ),
        *history.messages[1:],
        ChatMessage(
            role="user",
            content="Summarize the topic of above conversation in as few words as possible.",
        ),
    )

    return chat_completion(summarize_context_history)


def text_extract(query, text):
    """Extract points relevant to a query from text."""

    history = ChatHistory()
    history.add_messages(
        ChatMessage(
            role="system",
            content="You are a helpful assistant who follows instructions carefully.",
        ),
        ChatMessage(
            role="user",
            content=f"""Query: {query}\n\nPlease concisely rewrite the following text, extracting the points 
            most interesting, pertinent and important to the preceding query. Don't invent information. If there is no relevant information,
            be silent.\n\nText: {text}""",
        ),
    )
    return chat_completion(history)
