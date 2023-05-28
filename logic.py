import enterprise_costs as ec
import manage_costs_tables as mct

# Идем по полям и заполняем их из таблиц, а также сразу подгружаем дефолтные данные в другие поля после выбора

# Создаем менеджера для работы с записями о таблицах
manager = mct.CostsTablesManager("costs.json")

# --- Поле 1: Отрасль ведения хозяйственной деятельности ---
table_name = "salary"  # Можно не только из этой таблицы взять список отраслей
# Полный список наименований из колонки с названиями
names = manager.get_all_names_from_table(table_name)
# Отдаем имена на форму в первое поле (Список отраслей)
print(names)  # Вместо print как-то передаем на форму

# --- Поле 2: Штатная численность сотрудников --- Подгружаем после выбора отрасли среднее значение
chosen_industry = "Пищевая промышленность - Молочная отрасль "  # Здесь храним выбранную пользователем отрасль, здесь значение только для теста
table_name = "staff"
# Получаем файл с таблицей staff
filename = manager.get_filename_from(table_name)
# Получаем имя колонки с названиями
name = manager.get_name_from(table_name)
# Получаем номер колонки с конкретным числовым значением
value = manager.get_value_index_from(table_name)
# Получаем конкретные данные из физической таблицы на диске после выбора пункта
avg_staff = ec.EnterpriseCosts(
    name=chosen_industry,
    table_filename=filename,
    cost_index=value)

print(avg_staff.count_costs())  # Грузим это значение в поле №2 Штатная численность сотрудников

# --- Поле 3: Территория расположения производства ---
table_name = "cadastral"
# Полный список наименований из колонки с названиями
names = manager.get_all_names_from_table(table_name)
# Отдаем имена на форму в первое поле (Список отраслей)
print(names)  # Вместо print как-то передаем на форму

# --- Поля 4,5 заполняются пользователем здесь надо сохранить в переменные эти значения ---
land_area = 100  # Поле 4: Площадь земельного участка
area_capital_construction = 30  # Поле 5: Площадь объектов капитального строительства

# --- Поле 6: Предполагаемое к использованию оборудование ---
table_name = "machinery"  # Список оборудования и средних издержек
# Полный список наименований из колонки с названиями
names = manager.get_all_names_from_table(table_name)
# Отдаем имена на форму в поле 6 (Список оборудования)
print(names)  # Вместо print как-то передаем на форму

# --- Поле 7: Планируемый тип зданий и их площади --- !!! Странное поле, надо делить на два, пока ничего не делаю !!!

# --- Поле 8: Предоставление бухгалтерских услуг ---
table_name = "accounting"  # Цена бухгалтерских услуг по формам собственности
# Полный список наименований из колонки с названиями
names = manager.get_all_names_from_table(table_name)
# Отдаем имена
print(names)  # Вместо print как-то передаем на форму

# --- Поле 9: Оформление патента --- !!! Только если в поле 8 выбран тип ИП, тогда активизируем и заполняем !!!
table_name = "patenting"  # Цена патента (там в таблице хаос, потом будем ее прихорашивать)
# Полный список наименований из колонки с названиями
names = manager.get_all_names_from_table(table_name)
# Отдаем имена
print(names)  # Вместо print как-то передаем на форму

# --- Поле 10: Иное --- Пока никак не обрабатываем


# Функция для получения поля value для указанного выбора из таблицы
def get_value(choice, table):
    result = 0

    # Получаем файл с таблицей staff
    filename = manager.get_filename_from(table)
    # Получаем имя колонки с названиями
    name = manager.get_name_from(table)
    # Получаем номер колонки с конкретным числовым значением
    value = manager.get_value_index_from(table)
    # Получаем конкретные данные из физической таблицы на диске после выбора пункта
    avg_staff = ec.EnterpriseCosts(
        name=choice,
        table_filename=filename,
        cost_index=value)
    result = avg_staff.count_costs()  # Забираем value из таблицы
    return result

# Передаем из формы данные и считаем все издержки
def count(
        chosen_industry,  # выбранная отрасль в 1 поле
        staff,  # Численность сотрудников во 2 поле
        territory,  # Выбранная территория в 3 поле
        land_area,  # Поле 4: Площадь земельного участка
        area_capital_construction,  # Поле 5: Площадь объектов капитального строительства
        machine,  # Поле 6: Предполагаемое к использованию оборудование
        accounting_type,  # Поле 8: Тип бухгалтерских услуг
        patenting_type,  # Поле 9: Патент
        other=0,  # Пока просто плюсуем любое другое к общей сумме
    ):
    sum = 0  # Общая сумма
    report = {}
    # Зарплата
    staff_salary = get_value(chosen_industry, "salary") * staff  # Средняя зп * количество сотрудников
    report["Зарплата сотрудников"] = staff_salary
    sum += staff_salary
    # Страховые и пенсионные взносы
    insurance = staff_salary * 0.3  # 30% от ЗП - единая ставка
    sum += insurance
    report["Страховые взносы"] = insurance
    # Стоимость аренды земли
    land = get_value(territory, "cadastral") * land_area * 0.1  # 10% от кадастровой стоимости площади на цену метра
    report["Аренда земли"] = land
    sum += land
    # Стоимость капитального строительства
    capital_construction = area_capital_construction * get_value("cost", "construction")  # Там в таблице одна строка
    report["Стоимость капитального строительства"] = capital_construction
    sum += capital_construction
    # Стоимость оборудования
    machine_cost = get_value(machine, "machinery")
    report["Стоимость оборудования"] = machine_cost
    sum += machine_cost
    # Бухгалтерские услуги
    accounting_cost = get_value(accounting_type, "accounting")
    report["Бухгалтерские услуги"] = accounting_cost
    # Госпошлина за регистрацию
    registration_fee = 0
    if accounting_type.find("ИП") != -1:
        registration_fee = get_value("Юридическое лицо", "registration")
    else:
        registration_fee = get_value("Индивидуальный предприниматель", "registration")
    report["Госпошлина за регистрацию"] = registration_fee
    sum += registration_fee
    # Стоимость патента
    patenting_cost = 0
    patenting_cost = get_value(patenting_type, "patenting")
    report["Стоимость патента"] = patenting_cost
    sum += patenting_cost

    # Налоги

    # Налог в бюджет Москвы
    tax_moscow = get_value(chosen_industry, "tax_moscow")
    report["Налог в бюджет Москвы"] = tax_moscow
    sum += tax_moscow
    # Налог на прибыль
    tax_income = get_value(chosen_industry, "tax_income")
    report["Налог на прибыль"] = tax_income
    sum += tax_income
    # Налог на имущество
    tax_property = get_value(chosen_industry, "tax_property")
    report["Налог на имущество"] = tax_property
    sum += tax_property
    # Налог на землю
    tax_land = get_value(chosen_industry, "tax_land")
    report["Налог на землю"] = tax_land
    sum += tax_land
    # НДФЛ
    tax_personal_income = get_value(chosen_industry, "tax_personal_income")
    report["НДФЛ"] = tax_personal_income
    sum += tax_land
    # Налог транспорт
    tax_transport = get_value(chosen_industry, "tax_transport")
    report["Транспортный налог"] = tax_transport
    sum += tax_transport
    # Прочие налоги
    tax_other = get_value(chosen_industry, "tax_other")
    report["Прочие налоги"] = tax_other
    sum += tax_other

    # Прочие издержки
    report["Прочие издержки"] = other
    sum += other  # Остальные издержки

    return report, sum

