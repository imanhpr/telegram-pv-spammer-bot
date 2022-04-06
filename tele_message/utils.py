import csv
from collections import namedtuple
from pathlib import Path
from typing import Generator

from pyrogram import Client

from .configreader import PHONE_FILE_PATH
from .session_manager import SessionAgent

RawUser = namedtuple("RawUser", ["main_id", "message", "picture", "username"])


def phone_csv_reader(filepath: Path) -> Generator[tuple, None, None]:
    with filepath.open("r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield (
                row["country_code"],
                row["phone_number"],
                row["api_id"],
                row["api_hash"],
                row["sms_rule"],
            )


def users_csv_reader(filepath: Path) -> Generator[RawUser, None, None]:
    with filepath.open("r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield RawUser(**row)


def make_sessions() -> list[SessionAgent]:
    """Make Sessions from csvfile and save tham
    then return the lost of them

    Returns:
        list[SessionAgent]: List of sessions
    """
    clients = []
    for row in phone_csv_reader(PHONE_FILE_PATH):
        code, number, api_id, hash, sms = row
        new_session = SessionAgent(
            phone_number=int(number),
            country_code=int(code),
            api_id=int(api_id),
            api_hash=hash,
            sms_rule=sms,
        )
        new_session.client()
        clients.append(new_session)
    return clients
