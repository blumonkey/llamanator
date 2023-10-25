from rich.console import Console
from rich.text import Text
from rich.style import Style
import readline  # needed to move the cursor using arrow keys
import sys


LIGHT_BLUE = "#A5E6F7"
LIGHT_YELLOW = "#FFF7DF"
bot_style = Style(color=LIGHT_BLUE, bold=True)
system_style = Style(color=LIGHT_YELLOW, bold=True)
console = Console(width=50, height=16)


def init_ui():
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=16, cols=50))


def show_spinner(context=""):
    return console.status(
        Text(context, style="italic green"),
        spinner="dots",
        spinner_style="status.spinner",
    )


def bot_print(str):
    console.print(str, style=bot_style)


def system_print(str):
    console.print(str, style=system_style)
