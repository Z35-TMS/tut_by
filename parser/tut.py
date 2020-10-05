import requests
from bs4 import BeautifulSoup as BS

#content-band > div.col-c > div > div.col-w > div.l-columns.air-30
class TutBy:
    __url = "https://news.tut.by/archive/{}.html"

    def __init__(self, date: str):
        self.__news = {}
        self.__date = date

    def get_page(self):
        root_page = requests.get(self.__url.format(self.__date))
        html = BS(root_page.text, features="html5lib")
        html = html.find("div", attrs={"id": "content-band"})
        html = html.find("div", attrs={"class": "l-columns"})
        b_news = html.find_all("div", attrs={"class": "b-news"})
        print(len(b_news))

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

    # def __getitem__(self, index):
    #     if isinstance(index, int):
    #         return self.__news[index]
    #     elif isinstance(index, str):
    #         raise KeyError(index)


if __name__ == "__main__":
    tut = TutBy("20.09.2020")
    # tut.parse()
    # for news in tut:
    #     print(news)
    tut.get_page()
