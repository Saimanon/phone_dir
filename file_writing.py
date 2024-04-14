from os.path import exists
from csv import DictReader, DictWriter, QUOTE_NONNUMERIC


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Не валидное имя")
            else:
                is_valid_first_name = True
        except NameError as err:
            print(err)
            continue

    last_name = "Иванов"

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


def create_file(file_name):
    # with - Менеджер контекста
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Номер'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el["Номер"] == str(lst[2]):
            print("Такой телофон уже есть")
            return
    obj = {"Имя": lst[0], "Фамилия": lst[1], "Номер": lst[2]}
    res.append(obj)
    with open(file_name, "a", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Номер'])
        f_writer.writerows(res)


file_name1 = 'phone.csv'
file_name2 = 'phone_new.csv'


def main():
    print('В этом проекте доступно два файла: phone.csv(1) и phone_new.csv(2)\nДоступные команды:')
    print('1.q - Выход')
    print('2.w - Запись строки в файл')
    print('3.r - Вывод содержимого файла')
    print('3.t - Перенос строки из одного файла в другой')
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            print('В какой из двух файлов хотите записать строку?')
            print('Введите 1, если в файл "phone.csv"')
            print('Введите 2, если в файл "phone_new.csv"')
            cmd = input('Введите 1 или 2\n')
            while cmd not in ('1', '2'):
                cmd = input('Необходимо ввести номера файлов: 1 - phone.csv или 2 - phone_new.csv\n')
            if cmd == '1':
                if not exists(file_name1):
                    create_file(file_name1)
                write_file(file_name1, get_info())
            else:
                if not exists(file_name2):
                    create_file(file_name2)
                write_file(file_name2, get_info())
        elif command == 'r':
            print('Содержимое какого из двух файлов хотите вывести?')
            print('Введите 1, если файла "phone.csv"')
            print('Введите 2, если файла "phone_new.csv"')
            cmd = input('Введите 1 или 2\n')
            while cmd not in ('1', '2'):
                cmd = input('Необходимо ввести номера файлов: 1 - phone.csv или 2 - phone_new.csv\n')
            if cmd == '1':
                if not exists(file_name1):
                    print("Файл отсутствует. Создайте его")
                    continue
                print(*read_file(file_name1))
            else:
                if not exists(file_name2):
                    print("Файл отсутствует. Создайте его")
                    continue
                print(*read_file(file_name2))
        elif command == 't':
            print('Содержимое из какого файла и какой строки необходимо перенести?')
            print('Введите 1, если из файла "phone.csv"')
            print('Введите 2, если если из файла "phone_new.csv"')
            cmd = input('Введите 1 или 2\n')
            while cmd not in ('1', '2'):
                cmd = input('Необходимо ввести номера файлов: 1 - phone.csv или 2 - phone_new.csv\n')
            file_from = open(file_name1 if cmd == "1" else file_name2, encoding="utf-8")
            file_to = open(file_name2 if cmd == "1" else file_name1, 'a', encoding="utf-8")
            nums = len(file_from.readlines())
            file_from.seek(0)
            print(f'В файле {nums} строк, строку с номером 1 переносить нельзя, там заголовки')
            n = int(input('Введите номер строки\n'))
            while n not in range(2, nums + 1):
                n = int(input(f'В файле {nums} строк, используйте номер от 2 до {nums} включительно \n'))
            data = file_from.readlines()[n - 1]
            file_to.write(data)
main()

