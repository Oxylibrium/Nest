#!/usr/bin/env python3

"""
Load and start the Nest client.
"""

import os
import logging

import yaml

from nest import client, helpers, exceptions

DEFAULTS = {
    "prefix": "nest!",
    "locale": "en_US",
}


def main():
    """
    Parse config from file or environment and launch bot.
    """
    logger = logging.getLogger()
    if os.path.isfile("config.yml"):
        logger.debug("Found config, loading...")
        with open("config.yml") as file:
            config = yaml.safe_load(file)
    else:
        logger.debug("Config not found, trying to read from env...")
        env = {
            key[8:].lower(): val
            for key, val in os.environ.items()
            if key.startswith("NESTBOT_")
        }
        config = {"tokens": {}, "settings": {}}

        for key, val in env.items():
            if key.startswith("token_"):
                basedict = config["tokens"]
                keys = key[6:].split("_")
            else:
                basedict = config["settings"]
                keys = key.split("_")

            pointer = helpers.dictwalk(
                dictionary=basedict, tree=keys[:-1], fill=True
            )

            if "," in val:
                val = val.split(",")

            pointer[keys[-1]] = val

    settings = {**DEFAULTS, **config["settings"], "tokens": config["tokens"]}

    bot = client.NestClient(**settings)

    if settings["database"]:
        bot.load_module("db")

    for module in os.listdir("modules"):
        # Ignore hidden directories
        if not module.startswith(".") and module != "db":
            try:
                bot.load_module(module)
            except exceptions.MissingFeatures as exc:
                if (
                    settings.get("database", None)
                    and exc.features != {"database"}
                ):
                    raise

    bot.run()


if __name__ == "__main__":
    main()
