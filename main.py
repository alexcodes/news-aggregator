from datetime import datetime, timedelta
import logging

import sched
import time
import urllib3

import envutil
from image.image_generator import ImageGenerator
from news.news_api import NewsApi
from news.news_storage import NewsStorage
from aggregator.aggregator import NewsAggregator


# Global things to do:
# TODO filter too small images
# TODO bad images replace by google search result
# TODO post news article
# TODO add hashtags
# TODO store news in db

def init_logging():
    # configure project logging
    logging.basicConfig(format='%(asctime)s %(levelname)-7s - %(message)s', level=logging.DEBUG)
    logging.info("Start VK_NEWS_AGGREGATOR")

    # configure libraries logging
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    init_logging()

    scheduler = sched.scheduler(time.time, time.sleep)
    priority = 1

    # env vars
    delay = envutil.get_update_frequency_sec()
    sources = envutil.get_sources()
    language = envutil.get_language()
    api_key = envutil.get_api_key()
    storage_filename = envutil.get_storage_filename()
    article_ttl = envutil.get_article_ttl_hours()
    font_filename = envutil.get_image_font_filename()
    default_image = envutil.get_default_image_filename()
    image_storage_path = envutil.get_image_storage_path()

    def time_function():
        timestamp = (datetime.utcnow() - timedelta(hours=article_ttl)).timestamp()
        return int(timestamp)

    news_api = NewsApi(sources, language, api_key)
    news_storage = NewsStorage(storage_filename, time_function)
    image_generator = ImageGenerator(font_filename, default_image, image_storage_path)
    news_aggregator = NewsAggregator(news_api, news_storage, image_generator)

    def repeat():
        news_aggregator.execute()
        scheduler.enter(delay, priority, repeat)

    try:
        scheduler.enter(0, priority, repeat)
        scheduler.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
