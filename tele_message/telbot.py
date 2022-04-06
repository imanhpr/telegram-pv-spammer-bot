from email import message
from enum import Enum
from pathlib import Path
from string import Template
from typing import NoReturn, Union

from pyrogram import Client
from pyrogram.types import User

from .configreader import PHOTOS_DIR
from .logconfig import logger_factory
from .report import write_csv_report
from .utils import users_csv_reader

logger = logger_factory(__name__)

BLOCKED_USER_STATUS = "long_time_ago"


class ErrorMessages(Enum):
    IS_BOT = "user {} is bot like me 🤪"
    IS_DELETED = "user {} has deleted his/her account 💀"
    IS_BLOCKED = "user {} has blocked me and i can't send message to him/her 😡"


class IsBlocked(Exception):
    pass


class IsBot(Exception):
    pass


class IsDeleted(Exception):
    pass


class SpamBot:
    def __init__(self, bot: Client) -> None:
        self.bot: Client = bot

    @staticmethod
    def _check_user(user: User) -> Union[User, NoReturn]:
        if user.is_deleted:
            raise IsDeleted()
        elif user.is_bot:
            raise IsBot()
        elif user.status == BLOCKED_USER_STATUS:
            raise IsBlocked()
        return user

    @staticmethod
    def _text_maker(main_text, **kwargs) -> str:
        return Template(main_text).substitute(**kwargs)

    def text_to_user(self, user: User, text: str, **kwargs) -> None:
        message = self._text_maker(text, **kwargs)
        log_message = f"Message has sent successfully to user {user.id}"
        try:
            if self._check_user(user):
                self.bot.send_message(chat_id=user.id, text=message)
                logger.info(log_message)
        except IsBlocked:
            logger.error(ErrorMessages.IS_BLOCKED.value.format(user.id))
        except IsDeleted:
            logger.error(ErrorMessages.IS_DELETED.value.format(user.id))
        except IsBot:
            logger.error(ErrorMessages.IS_BOT.value.format(user.id))

    def text_to_all(self):
        pass

    def tphoto_to_user(
        self, user: User, caption: str, photo_file: Path, **kwargs
    ) -> tuple[bool, str]:
        caption = self._text_maker(caption, **kwargs)
        flag = False
        log_message = f"Message has sent successfully to user {user.id}"
        try:
            if self._check_user(user):
                with photo_file.open("rb") as image:
                    self.bot.send_photo(user.id, caption=caption, photo=image)
                logger.info(log_message)
                flag = True
                message = "Success"
        except IsBlocked:
            logger.error(ErrorMessages.IS_BLOCKED.value.format(user.id))
            message = "Block"
        except IsDeleted:
            logger.error(ErrorMessages.IS_DELETED.value.format(user.id))
            message = "Deleted"
        except IsBot:
            logger.error(ErrorMessages.IS_BOT.value.format(user.id))
            message = "Bot"
        return flag, message

    def tphoto_to_all(self, user_csv: Path, **kwargs) -> None:
        fail_users = []
        for index, data in enumerate(users_csv_reader(user_csv), 1):
            logger.info(f"Message Number : {index}")
            if user := self.bot.get_users(data.main_id or data.username):
                p = PHOTOS_DIR.joinpath(data.picture)
                result = self.tphoto_to_user(user, data.message, p, **kwargs)
                message_state, reason = result
                if not message_state:
                    fail_users.append(
                        {
                            "main_id": user.id,
                            "user_name": user.username,
                            "user_status": user.status,
                            "reason": reason,
                            "picture": p.absolute(),
                            "message": data.message,
                        }
                    )
            logger.info("All messages has just sent.")
            fild_names = [
                "main_id",
                "user_name",
                "user_status",
                "reason",
                "picture",
                "message",
            ]
            name, report_path = write_csv_report(
                "unsuccessful_users_list", fild_names, fail_users
            )
            logger.info("A report of unsuccessful messages has been done")
            logger.info(f"Report Name is : {name}")
            logger.info(f"Report file path is : {report_path}")
