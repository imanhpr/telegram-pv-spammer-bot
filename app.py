import os
from enum import Enum
from pathlib import Path
from typing import Optional

from art import tprint
from PyInquirer import prompt
from pyrogram.errors import PeerIdInvalid
from rich.console import Console

from tele_message import __version__
from tele_message.configreader import (
    PHONE_FILE_NAME,
    PHONE_FILE_PATH,
    PHOTOS_DIR,
    ROOT_DIR,
    SESSIONS_DIR,
    USERS_FILE_PATH,
)
from tele_message.helper_script import dir_maker
from tele_message.report import write_csv_report
from tele_message.session_manager import SessionAgent
from tele_message.telbot import SpamBot
from tele_message.utils import csv_len, make_sessions, users_csv_reader

console = Console()


class MainMenuItems(Enum):
    SEND_TO_ALL = "Send message to all"
    MAKE_NEW_SESSIONS = "Make New Sessions"
    GENERATE_BASE_FOLDER = "Make Default Data Folder"

    EXIT = "Exit"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def welcome_message() -> None:
    FILL_CHR = "░"
    tprint("PV-Spam-Bot", font="tarty1")
    console.print(FILL_CHR * 89)
    console.print(
        f" Welcome To [red][bold]PV-Spam-Bot[/bold][/red] version {__version__} ".center(
            113,
            FILL_CHR,
        )
    )
    console.print(FILL_CHR * 89, "\n")


def main_menu() -> MainMenuItems:
    main_menu_question = [
        {
            "type": "list",
            "name": "main_menu_answer",
            "message": "Select : ",
            "choices": list(map(lambda x: x.value, MainMenuItems)),
        }
    ]
    raw_item = prompt(main_menu_question)["main_menu_answer"]
    return MainMenuItems(raw_item)


def yes_or_no(message: str) -> bool:
    question = [
        {
            "type": "confirm",
            "name": yes_or_no.__name__,
            "message": message,
        }
    ]
    answer = prompt(question)
    return answer[yes_or_no.__name__]


if __name__ == "__main__":
    cls()
    welcome_message()
    sessions: Optional[list[SessionAgent]] = None
    if not ROOT_DIR.exists():
        console.log("[bold][blue]ROOT_DIR[/blue][/bold] dose not exist !")
        console.log("Makeing [bold][blue]ROOT_DIR[/blue][/bold] ...")
        dir_maker()
        console.log(f"[bold][blue]ROOT_DIR[/blue][/bold] set : {ROOT_DIR}")
    while True:
        answer = main_menu()
        if answer == MainMenuItems.EXIT:
            console.log("Exit From Program ...")
            exit()
        elif answer == MainMenuItems.MAKE_NEW_SESSIONS:
            console.log(f"File Name Is : {PHONE_FILE_NAME}")
            console.log(f"Absolute File Path Is : {PHONE_FILE_PATH}")
            if yes_or_no("Do you want make sessions with this file ?"):
                console.log("Enter telegram login code for every number.")
                sessions = make_sessions()
                console.log(f"Sessions have just created in : {SESSIONS_DIR}")
                console.log("Back To Main Menu ...")
            else:
                console.log("Back To Main Menu ...")
                continue
        elif answer == MainMenuItems.SEND_TO_ALL:
            if not sessions:
                console.log("Please first sessions and Try agine.")
                console.log("Back To Main Menu ...")
                continue
            total_user = csv_len(USERS_FILE_PATH.open("r"))
            iter_sessions = iter(sessions)
            console.log(f"Total user number : {total_user}")
            unsuccessful_results = []
            for index, rawuser in enumerate(users_csv_reader(USERS_FILE_PATH), 1):
                console.log(f"User {index}/{total_user}")
                try:
                    agent = next(iter_sessions)
                except StopIteration:
                    iter_sessions = iter(sessions)
                    agent = next(iter_sessions)
                with agent.client() as cl:
                    spambot = SpamBot(cl)
                    try:
                        user = cl.get_users(rawuser.main_id or rawuser.username)
                    except PeerIdInvalid as e:
                        console.log(
                            f"User with id {rawuser.main_id or None} or {rawuser.username or None} Dosn't exsist"
                        )
                        console.log("Next ...")
                        continue
                    except Exception as e:
                        console.log("exception : ", e)
                    image = Path(PHOTOS_DIR, rawuser.picture)
                    result, reason = spambot.tphoto_to_user(
                        user, rawuser.message, image
                    )
                    if not result:
                        unsuccessful_results.append(
                            {
                                "main_id": user.id,
                                "user_name": user.username,
                                "user_status": user.status,
                                "reason": reason,
                                "picture": image.absolute(),
                                "message": rawuser.message,
                            }
                        )
            if unsuccessful_results:
                fild_names = [
                    "main_id",
                    "user_name",
                    "user_status",
                    "reason",
                    "picture",
                    "message",
                ]
                name, report_path = write_csv_report(
                    "unsuccessful_users_list", fild_names, unsuccessful_results
                )
                console.log("A report of unsuccessful messages has been done")
                console.log(f"Report Name is : {name}")
                console.log(f"Report file path is : {report_path}")
            else:
                console.log(
                    "We didn't have any problem and all messages have sent successfully"
                )
                console.log("Back To Main Menu ...")
