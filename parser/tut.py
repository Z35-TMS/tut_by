import requests
import threading
from bs4 import BeautifulSoup as BS
from concurrent.futures import ThreadPoolExecutor


class TutBy:
    __url = "https://news.tut.by/archive/{}.html"

    def __init__(self, date: str):
        self.__news = []
        self.__rubrics = {}
        self.__date = date

    @staticmethod
    def _get_news(url, result):
        try:
            result.append(requests.get(url).text)
        except Exception:
            pass

    @staticmethod
    def _get_news_pool(url):
        return requests.get(url).text

    def _run_load_news(self, urls):
        results = []
        threads = [
            threading.Thread(target=self._get_news, args=(url, results)) for url in urls
        ]
        _ = [worker.start() for worker in threads]
        _ = [worker.join() for worker in threads]
        return results

    def _run_load_news_pool(self, urls):
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(self._get_news_pool, urls)
            return results
        return []

    def get_rubrics(self):
        root_page = requests.get(self.__url.format(self.__date))
        html = BS(root_page.text, features="html5lib")
        html = html.find("div", attrs={"id": "content-band"})
        html = html.find("div", attrs={"class": "l-columns"})
        b_news = html.find_all("div", attrs={"class": "b-news"})
        for rubric in b_news:
            head_rubric = rubric.find("div", attrs={"class": "rubric-title"})
            rubric_name = head_rubric.text
            self.__rubrics[rubric_name] = []
            rubric_news = rubric.find_all("div", attrs={"class": "news-entry"})
            for r_news in rubric_news:
                a = r_news.find("a", attrs={"class": "entry__link"})
                self.__rubrics[rubric_name].append(a.attrs["href"])

    @staticmethod
    def _parse_news(html_text):
        html = BS(html_text, features="html5lib")
        head = html.find("div", attrs={"class": "m_header"})
        news_body = html.find("div", attrs={"id": "article_body"})
        news_p = news_body.find_all("p")
        text = "".join([p.get_text() for p in news_p])
        text = text.replace("\xa0", " ").replace("&nbsp;", " ")
        head = head.get_text()
        # if head is not None:
        #     head = head.get_text()
        # else:
        #     head = text.split(".")[0]
        return head, text


    def get_news(self):
        # news = [
        #     {"rubric": rubric, "texts": self._run_load_news(links)}
        #     for rubric, links in self.__rubrics.items()
        # ]
        news = [
            {"rubric": rubric, "texts": self._run_load_news_pool(links)}
            for rubric, links in self.__rubrics.items()
        ]
        for n in news:
            record = {"rubric": n["rubric"], "news": []}
            for text in n["texts"]:
                try:
                    head, text = self._parse_news(text)
                except AttributeError:
                    continue
                record["news"].append({"head": head, "text": text}) 
            self.__news.append(record)
        print(self.__news[0].keys())

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
    tut.get_rubrics()
    tut.get_news()
