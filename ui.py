from rich.console import Console
from rich.text import Text
from rich.style import Style
import os
import readline  # needed to move the cursor using arrow keys

"""
Everything related to the UI/styling.
"""

LIGHT_BLUE = "#A5E6F7"
LIGHT_YELLOW = "#FFF7DF"
bot_style = Style(color=LIGHT_BLUE, bold=True)
system_style = Style(color=LIGHT_YELLOW, bold=True)
debug_style = Style(color="white", bgcolor="red", bold=True)
console = Console(width=50, height=16)


def show_spinner(context=""):
    return console.status(
        Text(context, style="italic green"),
        spinner="dots",
        spinner_style="status.spinner",
    )


def bot_print(str):
    console.print(str, style=bot_style)


def debug_print(str):
    console.print(str, style=debug_style)


def system_print(str):
    console.print(str, style=system_style)


def print_sources(docs):
    console.print(
        f"{os.linesep}".join(
            [
                " - " + f"{d.metadata['page']}" + f"{d.metadata['source']}"
                for d in docs
            ]
        ),
        style=system_style,
    )
    return console.rule()
