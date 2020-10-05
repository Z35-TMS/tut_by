import re
from bs4 import BeautifulSoup as BS


class TutBy:
    __url = ""

    def __init__(self, date: str):
        self.__news = []

    def get_page(self):
        return None

    def parse_bs(self):
        pass

    def pars_re(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        for news in self.__news:
            yield news
        raise StopIteration