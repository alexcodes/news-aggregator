import logging

import requests

from news.article import Article


def check_ok_status(response_json):
    if response_json["status"] != "ok":
        raise RuntimeError(response_json["message"])


def filter_not_readable(articles):
    return [article for article in articles
            if is_readable(article.title) and is_readable(article.description)]


def is_readable(text):
    if not text:
        return True

    not_letter_count = 0
    for char in text:
        if not char.isalpha():
            not_letter_count += 1

    threshold = 0.5
    readable = not_letter_count / len(text) < threshold
    if not readable:
        logging.debug("Not readable: %s", text)
    return readable


class NewsApi:
    def __init__(self, sources, language, api_key):
        self.sources = sources
        self.language = language
        self.api_key = api_key

    def top(self):
        url = "https://newsapi.org/v2/top-headlines?sources={}&apiKey={}"\
            .format(self.sources, self.api_key)
        response = requests.get(url, verify=False)
        response_json = response.json()
        check_ok_status(response_json)

        articles_json = response_json["articles"]
        articles = [Article(
            item["source"]["id"],
            item["title"],
            item["description"],
            item["url"],
            item["urlToImage"],
            item["publishedAt"]
        ) for item in articles_json]

        articles = filter_not_readable(articles)

        return articles

    def get(self, timestamp_from):
        url = "https://newsapi.org/v2/everything?sources={}&from={}&language={}&apiKey={}"\
            .format(self.sources, timestamp_from, self.language, self.api_key)
        response = requests.get(url, verify=False)
        response_json = response.json()
        check_ok_status(response_json)

        articles_json = response_json["articles"]
        articles = [Article(
            item["source"]["id"],
            item["title"],
            item["description"],
            item["url"],
            item["urlToImage"],
            item["publishedAt"]
        ) for item in articles_json]

        articles = filter_not_readable(articles)

        return articles
