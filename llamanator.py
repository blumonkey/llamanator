import sys
from chat import setup_openai, complete
from ui import bot_print, system_print, init_ui


def parse_input():
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
    elif cleaned.startswith("/"):
        system_print("Unknown command: " + cleaned)
    else:
        response = complete(cleaned)
        bot_print(response)


def main():
    while True:
        try:
            parse_input()
        except (SystemExit, KeyboardInterrupt) as e:
            raise e


if __name__ == "__main__":
    init_ui()
    setup_openai("You are a helpful AI assistant that helps with programming tasks.")
    main()
