from pathlib import Path

from .configreader import *


def dir_maker() -> None:
    if not ROOT_DIR.exists():
        ROOT_DIR.mkdir()
        REPORTS_DIR.mkdir()
        SESSIONS_DIR.mkdir()
        ROOT_DIR.joinpath(USER_DATA_DIR_NAME).mkdir()
        PHOTOS_DIR.mkdir()
