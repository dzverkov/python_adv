import subprocess


# 1.Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.

print("\nTask 1\n---------------------------------------------------\n")

str1 = "разработка"
str2 = "сокет"
str3 = "декоратор"

print(f"str1 = {str1}, type = {type(str1)}")
print(f"str1 = {str2}, type = {type(str2)}")
print(f"str1 = {str3}, type = {type(str3)}")

b_str1 = str1.encode()
b_str2 = str2.encode()
b_str3 = str3.encode()

print(f"b_str1 = {b_str1}, type = {type(b_str1)}")
print(f"b_str1 = {b_str2}, type = {type(b_str2)}")
print(f"b_str1 = {b_str3}, type = {type(b_str3)}")

print(f"b_str1 decode = {b_str1.decode()}")
print(f"b_str2 decode = {b_str2.decode()}")
print(f"b_str3 decode = {b_str3.decode()}")

b_str1 = str1.encode("utf-8")
b_str2 = str2.encode("utf-8")
b_str3 = str3.encode("utf-8")

print(f"b_str1 utf-8 = {b_str1}")
print(f"b_str1 utf-8 = {b_str2}")
print(f"b_str1 utf-8 = {b_str3}")

print(f"b_str1 decode latin-1 = {b_str1.decode('latin-1')}")
print(f"b_str2 decode latin-1 = {b_str2.decode('latin-1')}")
print(f"b_str3 decode latin-1 = {b_str3.decode('latin-1')}")


# 2.Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих
# переменных.

print("\nTask 2\n---------------------------------------------------\n")

str1 = b"class"
str2 = b"function"
str3 = b"method"

print(f"str1 = {str1}, type = {type(str1)}, length = {len(str1)}")
print(f"str1 = {str2}, type = {type(str2)}, length = {len(str2)}")
print(f"str1 = {str3}, type = {type(str3)}, length = {len(str3)}")

# 3.Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

print("\nTask 3\n---------------------------------------------------\n")

print("Слова 'класс' и 'функция' нельзя представить в байтовом типе,т.к. содержат символы, не входящие в ASCII")

# 4.Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
# в байтовое и выполнить обратное преобразование (используя методы encode и decode).

print("\nTask 4\n---------------------------------------------------\n")

str1 = "разработка"
str2 = "администрирование"
str3 = "protocol"
str4 = "standard"

b_str1 = str1.encode()
b_str2 = str2.encode()
b_str3 = str3.encode()
b_str4 = str4.encode()

print(f"str1 encode = {b_str1}")
print(f"str2 encode = {b_str2}")
print(f"str3 encode = {b_str3}")
print(f"str4 encode = {b_str4}")

print(f"b_str1 decode = {b_str1.decode()}")
print(f"b_str2 decode = {b_str2.decode()}")
print(f"b_str3 decode = {b_str3.decode()}")
print(f"b_str4 decode = {b_str4.decode()}")

# 5.Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип
# на кириллице.

print("\nTask 5\n---------------------------------------------------\n")

res = ['yandex.ru', 'youtube.com']

for r in res:
    print(f"\nPing {r}")
    args = ['ping', r]
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
                line = line.decode('cp866').encode('utf-8')
                print(line.decode('utf-8').strip())

# 6.Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

print("\nTask 5\n---------------------------------------------------\n")

file_name = "Task6_file.txt";
with open(file_name, 'w') as f_n:
    f_n.write("сетевое программирование\nсокет\nдекоратор")
    print(f_n)

with open(file_name, 'r', encoding='utf-8', errors='replace') as f_n:
    for fl in f_n:
        print(fl)
