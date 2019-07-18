import csv
import json
import re
import yaml

'''
   1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
    файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

   2. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и
    считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения
    параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра
    поместить в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list,
    os_code_list, os_type_list. В этой же функции создать главный список для хранения данных отчета — например,
    main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС»,
    «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить
    в файл main_data (также для каждого файла);
    
   3. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
   данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;

   4. Проверить работу программы через вызов функции write_to_csv(). 
'''

def get_row_val(p_s):
    return re.sub(r'^.*:[ ]+', '', p_s)

def get_data():
    file_lst = ['./data/info_1.txt', './data/info_2.txt', './data/info_3.txt']
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    cols = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

    for f in file_lst:
        with open(f, 'r') as f_n:
            for row in f_n:
                row = row.strip()
                if row.find('Изготовитель системы') != -1:
                    os_prod_list.append(get_row_val(row))
                elif row.find('Название ОС') != -1:
                    os_name_list.append(get_row_val(row))
                elif row.find('Код продукта') != -1:
                    os_code_list.append(get_row_val(row))
                elif row.find('Тип системы') != -1:
                    os_type_list.append(get_row_val(row))

    main_data = [cols, os_prod_list, os_name_list, os_code_list, os_type_list]
    return main_data


def write_to_csv(p_data, p_file):
    with open(p_file, 'w', newline='') as f:
        f_writer = csv.writer(f)
        # Сохраняем заголовок
        f_writer.writerow(p_data[0])
        # Сохраняем остальные данные
        for r in zip(p_data[1], p_data[2], p_data[3], p_data[4]):
            f_writer.writerow(r)

'''
   5. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
   Написать скрипт, автоматизирующий его заполнение данными. Для этого:

   6. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
   цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в
   файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;

   7. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
'''

def write_order_to_json(p_item, p_quantity, p_price, p_buyer, p_date):
    order_dict = {
        "item": p_item,
        "quantity": p_quantity,
        "price": p_price,
        "buyer": p_buyer,
        "date": p_date
    }

    with open('./data/orders.json', 'w') as f:
        json.dump(order_dict, f, ensure_ascii=False, indent=4)

'''
   8. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных
   в файле YAML-формата. Для этого:

   9. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
   второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число
   с юникод-символом, отсутствующим в кодировке ASCII (например, €);

   10. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию
   файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом:
   allow_unicode = True;

   11. Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''

def write_order_to_yaml(p_data):

    with open('./data/file.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(p_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def load_order_from_yaml():

    with open('./data/file.yaml', 'r', encoding='utf-8') as f:
        p_data = yaml.load(f, yaml.Loader)
    return p_data


# Задание на закрепление знаний по модулю CSV
write_to_csv(get_data(), './data/main_data.csv')
# Задание на закрепление знаний по модулю json
write_order_to_json(p_item='Велосипед'
                    , p_quantity=1
                    , p_price=7500
                    , p_buyer='Покупатель 1'
                    , p_date='01.10.2018'
                    )
# Задание на закрепление знаний по модулю yaml
order_dict = {
    "items": ['Велосипед', 'Самокат', 'Фонарик'],
    "quantity": 3,
    "buyer": {'1€': 'Покупатель', '2€': 'Адрес 1', '3€': 'Домофон 77'}
}
print(order_dict)
write_order_to_yaml(order_dict)
f_order_dict = load_order_from_yaml()
print(f_order_dict)
