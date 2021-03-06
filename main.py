import logging
import sched
import time
from datetime import datetime, timedelta

import urllib3

import envutil
from aggregator.aggregator import NewsAggregator
from image.image_generator import ImageGenerator
from news.news_api import NewsApi
from news.news_storage import NewsStorage


# Global things to do:
# TODO limit 50 posts/day
# TODO filter too small images
# TODO bad images replace by google search result
# TODO generate guid for vk_post
# TODO add hashtags
# TODO store news in db
from vk.vk import VK


def init_logging():
    # configure project logging
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(module)s:%(lineno)s - %(message)s', level=logging.DEBUG)
    logging.info("Start VK_NEWS_AGGREGATOR")

    # configure libraries logging
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)
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
    vk_access_token = envutil.get_vk_access_token()
    vk_target_group = envutil.get_vk_target_group()

    def time_function():
        timestamp = (datetime.utcnow() - timedelta(hours=article_ttl)).timestamp()
        return int(timestamp)

    news_api = NewsApi(sources, language, api_key)
    news_storage = NewsStorage(storage_filename, time_function)
    image_generator = ImageGenerator(font_filename, default_image, image_storage_path)
    vk_api = VK(vk_access_token, vk_target_group)
    news_aggregator = NewsAggregator(news_api, news_storage, image_generator, vk_api)

    def repeat():
        try:
            news_aggregator.execute()
        except Exception as e:
            logging.error(e)
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
