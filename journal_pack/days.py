import datetime
import os
from time import localtime, time
from .entries import Entry


def reader_text() -> tuple[bool, str]:
    """
    Функция считывает набор введенных строк и преобразует их
    в 1 строку, которую возвращает

    :return: (str) строка введенного текста
    """
    os.system('cls')
    print("Введите текст  (stop - конец, cansel - отмена)\n")
    text = ''
    is_continue = False
    while True:
        line = input('> ')
        if line.lower() == 'stop':
            is_continue = True
            break
        if line.lower() == 'cansel':
            is_continue = False
            break
        text += line + '\n'
    return is_continue, text


def week_name(day_number: int) -> str:
    """
    Возвращает название дня недели по его номеру

    :param day_number: (int) номер дня в недели (1 - 6)
    :return: (str) название дня недели
    """
    day_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return day_names[day_number]


def red(text: str) -> str:
    """Окраска текста в красный цвет"""
    return f"\033[1;31m{text}\033[0m"


class Day:
    """
    Класс "Day" ("День")

    Объект содержит в себе дату дня, данные о защищенности дня,
    список всех записей, данные о метке дня.

    Дата добавляется автоматически, основываясь на дату в ПК
    """

    def __init__(self) -> None:
        """
        Инициализация объекта Day.
        Устанавливает все доп значения в False для возможной будущей ручной настройки
        """
        self.date: dict = {'day': datetime.datetime.now().day,
                           'month': datetime.datetime.now().month,
                           'year': datetime.datetime.now().year,
                           'week_name': week_name(localtime(time())[6])}
        self.entries: list[Entry] = []
        self.marked: bool = False
        self.protected: bool = False

    def change_mark(self) -> None:
        """Изменение состояния метки"""
        self.marked = not self.marked

    def add_entry(self) -> None:
        """
        Добавляет в список entries новый объект Entry

        :return: None
        """
        is_continue, text = reader_text()
        if is_continue:
            new_entry = Entry(text=text)
            self.entries.append(new_entry)
            del new_entry
        del text, is_continue

    def view_entries(self, permission: bool = False) -> str:
        """
        Преобразовывает все записи в одну строку

        Если день защищен, возвращает "Доступ запрещен", иначе
        собирает текст всех записей в одну строку и возвращает ее

        :param permission: (bool) защита дня
        :return: (str) строка с записями дня, либо "Доступ запрещен"
        """
        if permission or not self.protected:
            text_of_entries = ''
            if len(self.entries) == 0:
                return "Записей нет\n"
            for i, entry in enumerate(self.entries):
                text_of_entries += entry.view_entry(number=i+1) + '\n'
            return text_of_entries
        return "Доступ запрещен\n"

    def view_day_info(self) -> str:
        date = f'{self.date['day']}.{self.date['month']}.{self.date['year']}'.ljust(11)
        marked = f'{(lambda x: '!' if x else '')(self.marked)}'.ljust(4)
        name = f'{self.date['week_name']}'.ljust(18)
        quantity = f'записей: {len(self.entries)}'.ljust(15)
        protected = f'{(lambda x: red('(protected)') if x else '')(self.protected)}'
        return date + marked + name + quantity + protected

    # Управление доступом

    def block(self) -> None:
        """Устанавливает объект Day как защищенный"""
        self.protected = True

    def unlock(self) -> None:
        """Устанавливает объект Day как общедоступный"""
        self.protected = False

    def block_entry(self, number: int) -> None:
        """
        Блокирует конкретную запись по порядковому номеру

        :param number: (int) порядковый номер записи
        :return: None
        """
        if number < len(self.entries):
            entry = self.entries[number]
            entry.block()

    def unlock_entry(self, number: int) -> None:
        """
        Открывает доступ к конкретной записи по порядковому номеру
        :param number: (int) порядковый номер записи
        :return: None
        """
        if number < len(self.entries):
            entry = self.entries[number]
            entry.unlock()

    # Сохранение данных

    def prep_day_to_json(self) -> dict:
        """
        Сворачивает данные объекта в словарь

        :return: (dict) вид: {"date": {date}, "entries": [entry_in_dict], "marked": "...", "protected": "..."}
        """
        entry_list = []
        for entry in self.entries:
            entry_list.append(entry.prep_entry_to_json())
        return {"date": self.date, "entries": entry_list, "marked": self.marked, "protected": self.protected}

    def day_data_from_json(self, data: dict) -> None:
        """
        Преобразует словарь обратно в объект "День" (Day)

        :param data: (dict) Словарь с данными
        """
        self.date = data["date"]
        self.marked = data["marked"]
        self.protected = data["protected"]

        for entry in data["entries"]:
            ret_entry = Entry()
            ret_entry.entry_data_from_json(data=entry)
            self.entries.append(ret_entry)
