import datetime
from .protected_pack import encoding, decoding


class Entry:
    """
    Класс "Entry" ("Запись").

    Объект содержит в себе текст записи, время создания записи и
    информации защите объекта.
    """

    def __init__(self, text: str = '', protected: bool = False) -> None:
        """
        Инициализация записи

        Принимает в себя текст записи и информацию о защите.
        Время устанавливается автоматически (текущее время на ПК)

        :param text: (str) текст записи
        :param protected: (bool) является ли запись защищенным объектом. По умолчанию False
        """
        self.time = f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute}"
        self.text = text
        self.protected = protected

    def view_entry(self, number: int, one_permission: bool = False) -> str:
        """
        Возвращает данные объекта, если он не защищен, иначе строку "Доступ запрещен"

        :param one_permission: (bool) разрешение на разовый просмотр
        :param number: (int) порядковый номер записи
        :return: (str) строку со временем и текстом записи (либо "Доступ запрещен")
        """
        if one_permission or not self.protected:
            text = self.time + '\n\n' + self.text + '\n' + ' '*35 + f"({number})\n" + '-' * 40
            return text
        else:
            return "Доступ запрещен" + '\n' + ' '*35 + f"({number})\n" + '-'*40

    # Управление доступом

    def block(self) -> None:
        """Устанавливает объект Entry как защищенный"""
        self.protected = True

    def unlock(self) -> None:
        """Устанавливает объект Entry как общедоступный"""
        self.protected = False

    # Сохранение данных

    def prep_entry_to_json(self) -> dict:
        """
        Сворачивает данные объекта в словарь для дальнейшей конвертации в json-объект.

        :return: (dict) Словарь с ключами: time(время), text(текст), protected(защита)
        """
        return {"time": self.time, "text": encoding(self.text), "protected": self.protected}

    def entry_data_from_json(self, data: dict) -> None:
        """
        Преобразует словарь обратно в объект "Запись" (Entry)

        :param data: (dict) Словарь с данными
        """
        self.time = data["time"]
        self.text = decoding(data["text"])
        self.protected = data["protected"]
