import logging


class NewsStorage:
    def __init__(self, filename, time_function):
        self.filename = filename
        self.time_function = time_function
        self.storage = []

    def filter_and_save(self, articles):
        filtered = self._filter(articles)
        self._save(filtered)
        return filtered

    def _filter(self, articles):
        # return articles that are not in the storage
        return [article for article in articles if not self._contains(article)]

    def _save(self, articles):
        if not articles:
            return

        self._remove_outdated()
        self.storage.extend(articles)
        self._persist()

    def _remove_outdated(self):
        min_timestamp = self.time_function()
        old_size = len(self.storage)

        self.storage = [article for article in self.storage if article.timestamp > min_timestamp]

        removed_count = old_size - len(self.storage)
        if removed_count:
            logging.debug("Remove outdated articles: %d", removed_count)

    def _persist(self):
        pass

    def _contains(self, article):
        for a in self.storage:
            if article.url == a.url:
                return True
        return False
