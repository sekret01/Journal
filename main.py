from journal_pack import Journal, admin_confirmation, confirmation
from backup.backup import backup_data
from time import sleep
import os

# from test import del_day, change_day


journal: Journal
Admin: bool = False
input_console = f"{(lambda x: 'Admin' if x else '')(Admin)}#>> "

def clear():
    os.system('cls')


# Просмотр дней и взаимодействие с ними

def view_days(marked: bool, admin: bool = False):
    """Начальный ввод даты, к которой надо перейти"""
    global input_console
    while True:
        clear()
        print(journal.view_journal(marked=marked))
        inp_date = input('\n' + input_console)
        if len(inp_date.split('.')) == 3:
            date = inp_date.split('.')
            for month in journal.months:
                for day in month.days:
                    if (day.date['day'] == int(date[0]) and
                        day.date['month'] == int(date[1]) and
                        day.date['year'] == int(date[2])):
                        ind = (journal.months.index(month), month.days.index(day))
                        day_page(ind=ind)
        elif inp_date == '0000':
            # сегодняшний день
            day_page((len(journal.months) - 1, len(journal.months[-1].days) - 1))
        elif inp_date == '':
            break


def day_page(ind: tuple[int, int]):
    """Вывод информации о выбранном дне"""
    while True:
        clear()
        text = journal.months[ind[0]].days[ind[1]].view_day_info() + '\n' + '-' * 60 + '\n\n'
        text += journal.months[ind[0]].days[ind[1]].view_entries()
        print(text)
        ind, stop, command = scroll_days(ind=ind)
        if stop:
            break
        if command == 'view_commands':
            command_page(ind=ind, text=text)


def scroll_days(ind: tuple[int, int]) -> tuple[tuple[int, int], bool, str]:
    """Перелистывание дней назад и вперед, проверка команд"""
    if ind == (0, 0):
        text = f"1 - далее\n3 - выход\n4 - команды\n\n{input_console}"
        next_step = (1, 0)
    elif ind == (len(journal.months) - 1, len(journal.months[-1].days) - 1):
        text = f"2 - назад\n3 - выход\n4 - команды\n\n{input_console}"
        next_step  =(0, 1)
    else:
        text = f"1 - далее\n2 - назад\n3 - выход\n4 - команды\n\n{input_console}"
        next_step = (1, 1)

    command = input(text)

    if command == '1':
        if next_step[0]:
            new_ind = is_other_month((ind[0], ind[1]), True)
            return new_ind, False, ''
    elif command == '2':
        if next_step[1]:
            new_ind = is_other_month((ind[0], ind[1]), False)
            return new_ind, False, ''
    elif command == '3':
        return ind, True, ''
    elif command == '4':
        return ind, False, 'view_commands'
    return ind, False, ''


def command_page(ind: tuple[int, int], text: str) -> None:
    """Работа с командами, взаимодействующими с днем и записями (Day, Entry)"""
    clear()
    print(text)
    if is_admin():
        com = input(f"1 - открыть страницу\n" +
                    f"2 - изменить метку\n" +
                    f"3 - разблокировать день".ljust(30) + f"4 - разблокировать запись\n" +
                    f"5 - заблокировать день".ljust(30) + "6 - заблокировать запись" +
                    f"\n\n{input_console}")
    else:
        com = input(f"1 - открыть страницу\n2 - изменить метку\n\n{input_console}")
    if com == '1':
        if journal.months[ind[0]].days[ind[1]].protected:
            permission, text = confirmation()
            if permission:
                clear()
                print(f"\n\033[32;1m>>>  {text}  <<<\033[0m".rjust(50) + '\n')
                print(journal.months[ind[0]].days[ind[1]].view_entries(permission=permission))
                _ = input()
            else:
                clear()
                print(text)
                sleep(1)

    elif com == '2':
        journal.months[ind[0]].days[ind[1]].change_mark()

    if is_admin():
        if com == '3':
            journal.months[ind[0]].days[ind[1]].unlock()
        elif com == '4':
            number = input("Номер записи: ")
            if number.isdigit():
                journal.months[ind[0]].days[ind[1]].unlock_entry(number=int(number) - 1)
        elif com == '5':
            journal.months[ind[0]].days[ind[1]].block()
        elif com == '6':
            number = input("Номер записи: ")
            if number.isdigit():
                journal.months[ind[0]].days[ind[1]].block_entry(number=int(number) - 1)


# Проверки

def is_other_month(ind: tuple[int, int], plus: bool) -> tuple[int, int]:
    """Проверка, наступил ли следующий месяц"""
    if plus:
        if len(journal.months[ind[0]].days) - 1 < ind[1] + 1:
            return ind[0] + 1, 0
        return ind[0], ind[1] + 1
    else:
        if ind[1] - 1 < 0:
            return ind[0] - 1, len(journal.months[ind[0]-1].days) - 1
        return ind[0], ind[1] - 1


def is_admin() -> bool:
    """Проверка, активированы ли права админа"""
    global Admin
    return True if Admin else False


def change_console_input():
    """Изменение ввода в консоли в зависимости от Admin"""
    global input_console
    input_console = f"{(lambda x: 'Admin' if x else '')(Admin)}#>> "


# основной интерфейс

def menu():
    """Главное меню приложения"""
    global journal, Admin, input_console
    date, week_name = journal.view_date_now()
    while True:
        clear()
        text = ("\n\n" +
                "1 - Добавить запись".ljust(50) + f"{date}\n" +
                "2 - Просмотр дней".ljust(50) + f"{week_name}\n" +
                "3 - Просмотр помеченных дней".ljust(50) + f"Записей: {len(journal.months[-1].days[-1].entries)}\n" +
                "4 - \n" +
                "5 - Выход\n\n" +
                f"{input_console}")

        command = input(text)
        if command == '1':
            journal.months[-1].days[-1].add_entry()
        if command == '2':
            view_days(marked=False)
        if command == '3':
            view_days(marked=True)
        if command == '4':
            pass
        if command == '5':
            break
        if command == "admin_activate":
            clear()
            permission, text = admin_confirmation()
            if permission:
                Admin = True
                change_console_input()
            print(text)
            sleep(1)
        if command in ["deactivate", "deactive"]:
            Admin = False
            change_console_input()


def main():
    global journal

    journal = Journal()
    menu()
    journal.journal_to_json()
    try:
        backup_data()
    except Exception as ex:
        _ = input(ex)


if __name__ == '__main__':
    main()
