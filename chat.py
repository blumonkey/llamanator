import openai
from ui import show_spinner
import logging
from data import ChatHistory, ChatMessage
import os


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


history = ChatHistory(max_length=100)


def setup_openai(system_prompt):
    openai.api_base = OPENAI_API_BASE
    openai.api_key = OPENAI_API_KEY
    history.add_message(ChatMessage(role="system", content=system_prompt))


def complete(prompt):
    with show_spinner():
        if history.is_too_long():
            summarize_context()
        history.add_message(ChatMessage(role="user", content=prompt))
        response_text = chat_completion(history)
        history.add_message(ChatMessage(role="assistant", content=response_text))
        return response_text


def summarize_context():
    global history
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

    response_text = chat_completion(summarize_context_history)
    system_prompt = (
        history.messages[0].content
        + f". Here is a summary of the conversation so far: {os.linesep}"
        + response_text
    )
    history = ChatHistory(max_length=1900)
    history.add_messages(
        ChatMessage(role="system", content=system_prompt),
    )


def chat_completion(history, model=OPENAI_API_KEY, temperature=0.6, max_tokens=1900):
    response = openai.ChatCompletion.create(
        model=model,
        messages=history.get_wire_format(),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
