import csv
from pathlib import Path
from typing import Generator

from .session_manager import SessionAgent


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


def make_sessions():
    clients = []
    for row in phone_csv_reader(Path("user_data/phone.csv")):
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
