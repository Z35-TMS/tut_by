import re
from bs4 import BeautifulSoup as BS


class TutBy:
    __url = ""

    def __init__(self, date: str):
        self.__news = []

    def get_page(self):
        return None

    def parse(self):
        pass

    def __iter__(self):
        self.__cursor = 0
        return self

    def __next__(self):
        if self.__cursor < len(self.__news):
            try:
                return self.__news[self.__cursor]
            finally:
                self.__cursor += 1
        self.__cursor = 0
        raise StopIteration

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.__news[index]
        elif isinstance(index, str):
            raise KeyError(index)


if __name__ == "__main__":
    tut = TutBy("20.09.2020")
    tut.parse()
    for news in tut:
        print(news)
    