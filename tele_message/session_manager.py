from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from pyrogram import Client, idle

SESSION_DIR: Path = Path(".").joinpath("number_sessions")


@dataclass()
class SessionAgent:
    phone_number: int
    country_code: int
    api_id: int
    api_hash: str
    sms_rule: bool = False
    _cl: Optional[Client] = field(init=False, default=None)

    @property
    def full_number(self) -> str:
        return str(self.country_code) + str(self.phone_number)

    def client(self) -> Client:
        if self._cl:
            return self._cl
        cl = Client(
            session_name=self.full_number,
            phone_number=self.full_number,
            api_hash=self.api_hash,
            api_id=self.api_id,
            force_sms=self.sms_rule,
            workdir=SESSION_DIR,
        )
        cl.start()
        cl.stop()
        self._cl = cl
        return cl
