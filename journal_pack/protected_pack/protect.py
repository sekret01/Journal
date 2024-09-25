import os
import threading
import configparser
from time import sleep


path = "journal_pack/protected_pack/configurate.ini"   # путь относительно main.py
conf = configparser.ConfigParser()
conf.read(path)

PASSWORD = conf.get("ADMIN", "password")
ADMIN_PASSWORD = conf["ADMIN_ALL_PRIVILEGE"]["password"]



ALL_BLOCK = False
block_time = 60
time_remaining = int(conf["ADMIN_ALL_PRIVILEGE"]["block_time"])



def red(text: str) -> str:
    """Окраска текста в красный цвет"""
    return f"\033[1;31m{text}\033[0;0;0m"


def confirmation() -> tuple:

    global PASSWORD, time_remaining
    if ALL_BLOCK:
        return False, red(f"Блокировка на {time_remaining} сек")

    os.system('cls')
    pwd = input("Введите пароль: ")
    if pwd == PASSWORD:
        return True, "Доступ разрешен"
    else:
        return False, "Доступ запрещен"


def admin_confirmation() -> tuple:

    global ADMIN_PASSWORD, time_remaining
    if ALL_BLOCK:
        return False, red(f"Блокировка на {time_remaining} сек")

    falls = 0
    while falls < 3:
        os.system('cls')
        pwd = input(f"Попыток: {3 - falls}\n\nВведите админ-пароль: ")
        if pwd == ADMIN_PASSWORD:
            falls = 0
            return True, "Доступ разрешен"
        else:
            falls += 1
    os.system('cls')
    timer = threading.Thread(target=blocker, name="blocker", daemon=True)
    timer.start()
    return False, red(f"Блокировка на {time_remaining} сек")


def blocker():

    global ALL_BLOCK, block_time, time_remaining
    ALL_BLOCK = True
    for i in range(block_time):
        sleep(1)
        time_remaining -= 1
    ALL_BLOCK = False
    time_remaining = block_time
