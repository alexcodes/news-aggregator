from datetime import datetime, timedelta
import logging

import sched
import time
import urllib3

import envutil
from news.newsApi import NewsApi


def init_logging():
    # configure project logging
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)-7s - %(message)s', level=logging.INFO)
    logging.info("Start VK_NEWS_AGGREGATOR")

    # configure libraries logging
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    init_logging()

    scheduler = sched.scheduler(time.time, time.sleep)
    priority = 1
    delay = envutil.get_update_frequency_sec()
    sources = envutil.get_sources()
    language = envutil.get_language()
    api_key = envutil.get_api_key()

    news_api = NewsApi(sources, language, api_key)

    def repeat():
        articles = news_api.top()

        # timestamp_from = datetime.utcnow() - timedelta(hours=4)
        # timestamp_from = timestamp_from.replace(microsecond=0).isoformat()
        # articles = news_api.get(timestamp_from)

        for article in articles:
            print(article.publishedAt, article.source, article.title, article.url)
        print("#" * 40)
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
