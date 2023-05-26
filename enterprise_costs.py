import pandas as pd


class EnterpriseCosts:

    def __init__(self, **kwargs):
        self.table = pd.DataFrame()
        self.table_filename = ""
        dict_ = {"name": "name",
                 "table_filename":"",
                 "cost_index": 2}
        self.__dict__ = kwargs
        for key, value in dict_.items():
            self.__dict__[key] = self.__dict__.get(key, value)
        if len(self.table_filename) > 0:
            self.load_table(self.table_filename)

    # Установка индекса колонки цены
    def set_cost_index(self, cost_index):
        self.cost_index = cost_index

    # Установка имени колонки с названием издержки
    def set_name(self, name):
        self.name = name

    # Грузим таблицу (Датафрейм) из стандартизированного файла
    def load_table(self, filename):
        self.table = pd.read_excel(filename)

    # Устанавливаем таблицу как датафрейм
    def set_table(self, table: pd.DataFrame):
        self.table = table

    # Расчет расходов
    def count_costs(self):
        # Находим строку с выбранным типом в колонке name и в полученном
        # датафрейме уже находим ячейку под номером cost_index
        cost = self.table.loc[self.table["name"] == self.name].iloc[:, self.cost_index]
        print(cost)
        return cost  # Возвращаем значение расходов
