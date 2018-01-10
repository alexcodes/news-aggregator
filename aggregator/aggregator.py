import logging


class NewsAggregator:
    def __init__(self, news_api, news_storage):
        self.news_api = news_api
        self.news_storage = news_storage
        self.count = 0

    def execute(self):
        logging.info("#" * 40)
        self.count = self.count + 1

        articles = self.news_api.top()
        articles = self.news_storage.filter_and_save(articles)

        if not articles:
            logging.info("No new articles, skip processing")
            return

        if self.count == 1:
            logging.info("Skip first batch")
            return

        logging.info("New articles: %d", len(articles))
        for article in articles:
            self._process_article(article)

    def _process_article(self, article):
        logging.info(str(article))
