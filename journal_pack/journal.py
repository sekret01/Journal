from .months import Month, name_month
from .days import week_name
from time import localtime, time, sleep
import threading
import datetime
import json


class Journal:
    def __init__(self) -> None:
        """
        Инициализация объекта Journal (Журнал)

        При старте инициализации объект устанавливает параметры по умолчанию, после чего
        пытается найти файл с сохраненными данными. Если таковые имеются, происходит их запись в объект и дальнейшая работа с ними.

        Так же запускается отдельный поток для проверки наступления нового дня и месяца.
        """
        self.months: list[Month] = []
        self.date_now: dict = {"day": datetime.datetime.now().day,
                               "month": datetime.datetime.now().month,
                               "year": datetime.datetime.now().year,
                               "week_name": week_name(localtime(time())[6])}
        self.journal_from_json()
        self.create_thread()

    # Авто настройка дат

    def create_thread(self) -> None:
        """
        Создание потока для отслеживания времени.

        Раз в один тик (установленное время) происходит проверка на равенство последнего месяца и дня с нынешними.
        Если есть изменения, программа вызовет функцию для добавления нового дня или месяца, в зависимости от того,
        что изменилось

        :return: None
        """
        def keep_track_of_time() -> None:
            while True:
                month_now = {'month': datetime.datetime.now().month,
                             'year': datetime.datetime.now().year,
                             'name_month': name_month(datetime.datetime.now().month)}
                day_now = {'day': datetime.datetime.now().day,
                           'month': datetime.datetime.now().month,
                           'year': datetime.datetime.now().year,
                           'week_name': week_name(localtime(time())[6])}
                if month_now != self.months[-1].date:
                    self.add_month()
                if len(self.months[-1].days) == 0 or day_now != self.months[-1].days[-1].date:
                    self.months[-1].add_day()
                    self.date_now = day_now
                self.journal_to_json()
                sleep(3)

        # Создание потока

        thr = threading.Thread(target=keep_track_of_time, name='thr_keep_track_of_time', daemon=True)
        thr.start()

    def add_month(self) -> None:
        """Добавляет новый месяц"""
        if len(self.months) == 0 or self.is_new_month():
            month = Month()
            self.months.append(month)

    def is_new_month(self) -> bool:
        """
        Проверка на наступление нового месяца

        Смотрятся данные о последнем месяце.
        Если данные о месяце не совпадают с настоящей датой (дата на ПК) -> True
        Иначе -> False
        """
        month_now = {'month': datetime.datetime.now().month,
                    'year': datetime.datetime.now().year,
                    'name_month': name_month(datetime.datetime.now().month)}
        if month_now != self.months[-1].date:
            return True
        return False

    # Основные функции для интерфейса

    def view_journal(self, marked: bool) -> str:
        text = ''
        for month in self.months:
            text += month.view_days(marked=marked)
        return text

    def view_date_now(self) -> tuple[str, str]:
        """Возвращает строку с нынешней датой"""
        return (f"{self.date_now["day"]}.{self.date_now["month"]}.{self.date_now["year"]}",
                f"{self.date_now["week_name"]}")

    # Сохранение данных

    def journal_to_json(self) -> None:
        month_list = []
        for month in self.months:
            month_list.append(month.prep_month_to_json())
        journal_dict = {"date_now": self.date_now, "months": month_list}
        with open('./journal_pack/data/data.json', 'w') as f:
            json.dump(journal_dict, f)

    def journal_from_json(self) -> None:
        with open('./journal_pack/data/data.json', 'r') as f:
            data = json.load(f)
        self.date_now = data["date_now"]
        for month in data["months"]:
            ret_month = Month()
            ret_month.month_data_from_json(data=month)
            self.months.append(ret_month)
