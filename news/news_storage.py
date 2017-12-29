class NewsStorage:
    def __init__(self, filename):
        self.filename = filename
        self.storage = []

    def add(self, articles):
        pass

    def filter(self, articles):
        return [article for article in articles if not self.contains(article)]

    def contains(self, article):
        for a in self.storage:
            if article.url == a.url:
                return True
        return False
