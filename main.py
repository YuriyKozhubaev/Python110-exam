import json
import random
import re
import faker

from conf import MODEL


def fabdecor(maxlen):
    """
    фабрика декораторов для проверки валидацию книги заданной длины
    :param maxlen: ограничение по длине книги
    :return: декоратор
    """
    def valid(fn):
        """
        декоратор для проверки валидации книги
        :param fn: оборачиваемая функция
        :return: функцию обертку
        """
        def wrapper() -> str:
            """
            функция обертка
            :return: наименование книги после проверки
            """
            bookname_ = fn()
            if len(bookname_) > maxlen:
                raise ValueError("слишком длинное название книги")
            return bookname_
        return wrapper
    return valid


@fabdecor(30)
def gettitle() -> str:
    """
    функция генерирует наименование книги
    :return: строка с наименованием книги
    """
    with open("books.txt", encoding="utf-8") as booksname:
        titlevalue = booksname.read().split("\n")
    return titlevalue[random.randrange(len(titlevalue))]


def getyear() -> int:
    """
    функция генерирует год выпуска книги
    :return: год выпуска
    """
    year: int = random.randrange(1990, 2023)
    return year


def getpage() -> int:
    """
    функция генерирует количество страниц книги
    :return:количество страниц книги
    """
    page: int = random.randrange(50, 100)
    return page


def getisbn13() -> str:
    """
    функция генерирует международный стандартный книжный номер
    :return: международный стандартный книжный номер
    """
    faker_ = faker.Faker("ru")
    return faker_.isbn13()


def getrating() -> float:
    """
    функция генерирует рейтинг книги
    :return: рейтинг книги
    """
    rating: float = random.uniform(0, 5)
    return round(rating, 2)


def getprice() -> float:
    """
    функция генерирует стоимость книги
    :return: стоимость книги
    """
    price: float = random.uniform(100, 10000)
    return round(price, 2)


def getauthor() -> list:
    """
    функция генерирует имя и фамилию автора книги
    :return: имя и фамилия автора книги
    """
    faker_ = faker.Faker("ru")
    authors = []
    for _ in range(random.randrange(1, 4)):
        if random.randrange(0, 2) == 0:
            name = faker_.first_name_female()
            surname = faker_.last_name_female()
        else:
            name = faker_.first_name_male()
            surname = faker_.last_name_male()
        authors.append(name + " " + surname)
    return authors


def booksgen(bookacount: int = 100, pk: int = 1) -> list:
    """
    функция возращает список книг
    :param bookacount:количество книг
    :param pk:порядковый номер книги
    :return:список словарей
    """
    bookslist = []
    for _ in range(bookacount):
        onebooksdict = {
            "model": MODEL,
            "pk": pk,
            "fields": {
                "title": gettitle(),
                "year": getyear(),
                "pages": getpage(),
                "isbn13": getisbn13(),
                "rating": getrating(),
                "price": getprice(),
                "author": getauthor()
            }
        }
        pk += 1
        bookslist.append(onebooksdict)
    return bookslist

def validate_isbn_13():
    """
    функция проверяет правильность структуры ISBN13
    :return: None
    """
    regul = r'(?:-13)?:?\x20*(?=.{17}$)97(?:8|9)([ -])\d{1,5}\1\d{1,7}\1\d{1,6}\1\d$'
    faker_ = faker.Faker("ru")
    for _ in range(1000000):
        if re.fullmatch(regul, faker_.isbn13()) is None:
            raise ValueError("ошибка в Isbn13")
    print("Ok")


if __name__ == "__main__":
    dictbooks = booksgen(100)
    with open("books.json", "w", encoding="utf-8") as bookvalue:
        json.dump(dictbooks, bookvalue, ensure_ascii=False, indent=4)
    validate_isbn_13()
