from api import chat_completion, prompt_completion
from data import ChatHistory, ChatType
from langchain.schema import HumanMessage, SystemMessage
from ui import debug_print

"""
Methods that perform specific tasks using the chat API, 
such as summarization or text extraction.
"""


def summarize_context(history, chat_type):
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
    if chat_type == ChatType.CHAT:
        return chat_completion(summarize_context_history)
    else:
        return prompt_completion(summarize_context_history.format())


def text_extract(query, text, chat_type):
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
    if chat_type == ChatType.CHAT:
        return chat_completion(history)
    else:
        return prompt_completion(history.format())


def __function_extract_chat(query, function):
    # TODO support multiple functions, optimize the prompt
    """Utilize provided to function to answer a query."""

    system_message = """
    You are a AI assistant who answers queries using the functions provieded. You will not provide any explanation for your answers. If the 
    query cannot be answered with the provided information, reply with "N/A". 

    Repeat, DO NOT PROVIDE ANY EXPLANATIONS OR CORRECTIONS IN YOUR RESPONSE, only respond with the funciton call or "N/A". 
    Here are some examples:

    Example 1:
    ----------

    Function: {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two integers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number to add",
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number to add",
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    Query: How do I add 75 and 144?

    Answer: add_numbers(75, 144)

    Example 2:
    ----------

    Function: {
        "type": "function",
        "function": {
            "name": "convert_to_uppercase",
            "description": "Converts a string to uppercase",
            "parameters": {
                "type": "object",
                "properties": {
                    "inp": {
                        "type": "string",
                        "description": "The string to convert to uppercase",
                    },
                },
                "required": ["inp"],
            },
        },
    }
    Query: Convert "Hello Barbie!" to uppercase.

    Answer: convert_to_uppercase("Hello Barbie!")
    """
    message_content = f"""
    Now here is the function and query you should answer:

    Function: {function.get_json()}
    Query: {query}

    Answer: 
    """
    debug_print(system_message)
    debug_print(message_content)
    history = ChatHistory()
    history.add_messages(
        SystemMessage(content=system_message),
        HumanMessage(content=message_content),
    )
    return chat_completion(history)


def function_extract(query, function, chat_type):
    """Utilize provided to function to answer a query."""

    if chat_type == ChatType.CHAT:
        return __function_extract_chat(query, function)
    else:
        system_message = "You are an intelligent AI agent that follows instructions carefully"
        message_content = f"""
        BEGININPUT
        BEGINCONTEXT
        ENDCONTEXT

        Given the following function, answer the query.

        Function: {function.get_json()}
        Query: {query}
        
        ENDINPUT
        BEGININSTRUCTION
        Answer the above query using the functions provided. You will not provide any explanation for your answers. If the 
        query cannot be answered with the provided information, reply with "N/A". 

        Repeat, DO NOT PROVIDE ANY EXPLANATIONS OR CORRECTIONS IN YOUR RESPONSE, only respond with the funciton call or "N/A". 
        ENDINSTRUCTION
        """

        debug_print(system_message)
        debug_print(message_content)
        history = ChatHistory()
        history.add_messages(
            SystemMessage(content=system_message),
            HumanMessage(content=message_content),
        )
        return prompt_completion(history.format())
