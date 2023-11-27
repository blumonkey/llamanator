import sys
from chat import Chat
from ui import bot_print, system_print
from documents import load_textfile, ingest_docs
from state import knowledge_store

"""
Main entry point for llamantor
"""


def parse_input(chat):
    try:
        user_input = input("> ")
        if user_input is None:
            return
    except EOFError:
        system_print("Bye!")
        sys.exit(0)

    cleaned = user_input.strip()
    if len(cleaned) == 0:
        return
    elif cleaned == "/quit" or cleaned == "/q":
        system_print("Bye!")
        sys.exit(0)
    elif cleaned.startswith("/ingest "):
        parts = cleaned.split(maxsplit=1)
        fname = parts[1]
        docs = load_textfile(fname)
        ingest_docs(fname, knowledge_store, docs)
    elif cleaned.startswith("/ask "):
        parts = cleaned.split(maxsplit=1)
        query = parts[1]
        response = chat.over_db(knowledge_store, query)
        bot_print(response)
    elif cleaned.startswith("/function "):
        parts = cleaned.split(maxsplit=1)
        query = parts[1]
        response = chat.over_function(query)
        bot_print(response)
    elif cleaned.startswith("/"):
        system_print("Unknown command: " + cleaned)
    else:
        response = chat.complete(cleaned)
        bot_print(response)


def main(chat):
    while True:
        try:
            parse_input(chat)
        except (SystemExit, KeyboardInterrupt) as e:
            raise e


if __name__ == "__main__":
    chat = Chat("You are a helpful AI assistant.")
    main(chat)
