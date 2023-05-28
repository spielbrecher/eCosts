import enterprise_costs as ec
import manage_costs_tables as mct

if __name__ == '__main__':
    import logic
'''
    # Создаем менеджера для работы с записями о таблицах
    manager = mct.CostsTablesManager("costs.json")

    table_name = "salary"

    # Получаем файл с таблицей для издержки Construction
    filename = manager.get_filename_from(table_name)

    # Получаем имя колонки с названиями
    name = manager.get_name_from(table_name)

    # Получаем номер колонки с конкретным числовым значением этой издержки
    value = manager.get_value_index_from(table_name)

    # Так мы узнаем полный список наименований из колонки с названиями видов издержек
    names = manager.get_all_names_from_table(table_name)
    # Отдаем имена на форму в первое поле (Список отраслей)
    print(names[0])

    # Получаем конкретные данные из физической таблицы на диске после выбора пункта
    construction_costs = ec.EnterpriseCosts(name=names[0],
                                            table_filename=filename,
                                            cost_index=value)

    # Считаем издержки
    print(construction_costs.count_costs())
'''


