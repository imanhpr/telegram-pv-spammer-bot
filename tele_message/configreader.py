import configparser
from pathlib import Path

CONFIG_DIR = Path(".").joinpath("config", "SpamBot.ini")
MAIN_CONFIG = configparser.ConfigParser()
MAIN_CONFIG.read(CONFIG_DIR)
