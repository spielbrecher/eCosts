# Менеджер таблиц с издержками
# Работает с json где лежит информация об имени файла нужной таблицы
# названии колонки типа издержки и номера колонки со значением издержки
import json
import pandas as pd


class CostsTablesManager:

    def __init__(self, filename):
        with open(filename, "r") as read_file:
            self.data = json.load(read_file)

    # Получаем имя файла для названия издержки
    def get_filename_from(self, cost_name):
        try:
            return self.data[cost_name]["file"]
        except:
            raise Exception("Проблема с поиском в costs.json")

    # Получаем имя колонки с названиями издержек
    def get_name_from(self, cost_name):
        try:
            return self.data[cost_name]["name"]
        except:
            raise Exception("Проблема с поиском в costs.json")

    # Получаем индекс колонки со значением издержки
    def get_value_index_from(self, cost_name):
        try:
            return int(self.data[cost_name]["value"])
        except:
            raise Exception("Проблема с поиском в costs.json")

    # Получаем все доступные имена из таблицы с именами издержек
    def get_all_names_from_table(self, name):
        # Получаем имя физической таблицы
        filename = self.get_filename_from(name)
        # Грузим физическую таблицу
        table = pd.read_excel(filename)
        # Узнаем имя колонки с названиями
        name_column = self.get_name_from(name)
        return table[name_column]
