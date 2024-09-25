import shutil

# пути для запуска из backup.py
SOURCE = ... # path to write backup
FILE_PATH = '../journal_pack/data/data.json'

# пути для запуска из main.py
OTHER_SOURCE = ... # path to read backup
OTHER_FILE_PATH = 'journal_pack/data/data.json'


def backup_data():
    shutil.copy(OTHER_FILE_PATH, OTHER_SOURCE)


def main():
    shutil.copy(FILE_PATH, SOURCE)


if __name__ == '__main__':
    main()
