import datetime
from .days import Day, week_name
from time import localtime, time


def name_month(number: int) -> str:
    month_names = ["Январь", "Февраль", "Март", "Апрель",
                   "Май", "Июнь", "Июль", "Август", "Сентябрь",
                   "Октябрь", "Ноябрь", "Декабрь"]
    return month_names[number-1]


def bold(text: str) -> str:
    """Возвращает жирный текст"""
    return f'\033[1m{text}\033[0;0;0m'


class Month:

    def __init__(self):
        self.date: dict = {'month': datetime.datetime.now().month,
                            'year': datetime.datetime.now().year,
                            'name_month': name_month(datetime.datetime.now().month)}
        self.days: list[Day] = []

    def add_day(self) -> None:
        if len(self.days) == 0 or self.is_new_day():
            day = Day()
            self.days.append(day)

    def is_new_day(self) -> bool:
        """
        Проверка на наступление нового дня

        Смотрятся данные о дате последнего записанного дня (в последнем записанном месяце).
        Если данные о дате дня не совпадают с настоящей датой (дата на ПК) -> True
        Иначе -> False
        """
        day_now = {'day': datetime.datetime.now().day,
                    'month': datetime.datetime.now().month,
                    'year': datetime.datetime.now().year,
                    'week_name': week_name(localtime(time())[6])}
        if day_now != self.days[-1].date:
            return True
        return False

    def view_days(self, marked: bool) -> str:
        text = '\n' + bold(f'==> {self.date["name_month"]} <==').rjust(45) + '\n\n'
        if marked:
            for day in self.days:
                if day.marked:
                    day_info = day.view_day_info()
                    text += '  ' + day_info + '\n'
            text += '\n' + '-' * 70 + '\n'
        else:
            for day in self.days:
                day_info = day.view_day_info()
                text += '  ' + day_info + '\n'
            text += '\n' + '-'*70 + '\n'
        return text

    # Сохранение данных

    def prep_month_to_json(self) -> dict:
        days_list = []
        for day in self.days:
            days_list.append(day.prep_day_to_json())
        return {"date": self.date, "days": days_list}

    def month_data_from_json(self, data: dict) -> None:
        self.date = data["date"]

        for day in data["days"]:

            ret_day = Day()
            ret_day.day_data_from_json(data=day)
            self.days.append(ret_day)

