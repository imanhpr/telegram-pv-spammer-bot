import configparser
from pathlib import Path


def make_defualt_config() -> None:
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()
    config = configparser.ConfigParser()
    config["FILE"] = {
        "root_dir": Path(".", "Data").absolute(),
        "users_file": "users.csv",
        "phones_file": "phone.csv",
    }
    with CONFIG_FILE.open("w") as configfile:
        config.write(configfile)


CONFIG_DIR = Path(".").joinpath("config")
CONFIG_FILE = CONFIG_DIR.joinpath("SpamBot.ini")

if not CONFIG_FILE.exists():
    make_defualt_config()

MAIN_CONFIG = configparser.ConfigParser()
MAIN_CONFIG.read(CONFIG_FILE)
USER_DATA_DIR_NAME = "user_data"
ROOT_DIR: Path = Path(MAIN_CONFIG.get("FILE", "root_dir"))
USERS_FILE_NAME: str = MAIN_CONFIG.get("FILE", "users_file")
USERS_FILE_PATH: Path = Path(
    ROOT_DIR.joinpath(USER_DATA_DIR_NAME).joinpath(USERS_FILE_NAME),
)
PHONE_FILE_NAME: str = MAIN_CONFIG.get("FILE", "phones_file")
PHONE_FILE_PATH: Path = Path(
    ROOT_DIR.joinpath(USER_DATA_DIR_NAME).joinpath(PHONE_FILE_NAME),
)
REPORTS_DIR: Path = ROOT_DIR.joinpath("reports")
SESSIONS_DIR: Path = ROOT_DIR.joinpath("sessions")
PHOTOS_DIR: Path = Path(
    ROOT_DIR.joinpath(USER_DATA_DIR_NAME).joinpath("photos"),
)
