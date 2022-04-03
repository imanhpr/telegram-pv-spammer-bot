from string import Template
from typing import Iterable

from pyrogram import Client
from pyrogram.types import InputPhoneContact, User


class SpamBot:
    def __init__(self, bot: Client) -> None:
        self.bot: Client = bot

    def add_contacts(self, contacts: Iterable) -> None:
        with self.bot:
            new_contancts = [InputPhoneContact(**contact) for contact in contacts]
            self.bot.import_contacts(list(new_contancts))

    def text_to_all(self, message: Template) -> None:
        with self.bot:
            contancts: list[User] = self.bot.get_contacts()
            for contact in contancts:
                self.bot.send_message(
                    contact.id,
                    text=message.substitute(
                        first_name=contact.first_name.capitalize(),
                        last_name=contact.last_name.capitalize(),
                    ),
                )

    def delete_all_contacts(self) -> None:
        with self.bot:
            user_ids = [user.id for user in self.bot.get_contacts()]
            self.bot.delete_contacts(user_ids)
