import toml


def get_config():
    """
    Reads config from TOML file
    """
    data = toml.load("config.toml")
    runtime = data["runtime"]
    bot = data["bots"][runtime["bot"]]
    return {
        "runtime": runtime,
        "bot": bot,
        "storage": data["storage"],
    }
