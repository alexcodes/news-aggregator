import logging

from vk.vk_post import VKPost


def _get_full_text(article):
    return "{}\n\n{}\n\nЧитать в источнике: {}"\
        .format(article.title, article.description, article.url)


class NewsAggregator:
    def __init__(self, news_api, news_storage, image_generator, vk_api):
        self.news_api = news_api
        self.news_storage = news_storage
        self.image_generator = image_generator
        self.vk_api = vk_api
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
            try:
                self._process_article(article)
            except Exception as e:
                logging.error(e)

    def _process_article(self, article):
        logging.info(str(article))
        img_file = self.image_generator.generate(article.title, article.url_to_image)
        full_text = _get_full_text(article)
        vk_post = VKPost(1, full_text, img_file)
        post_id = self.vk_api.post(vk_post)
        logging.info("Post published, id=%d", post_id)
