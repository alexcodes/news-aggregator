import news.time_utils as time_utils


class Article:
    def __init__(self, source, title, description, url, url_to_image, published_at):
        self.source = source
        self.title = title
        self.description = description
        self.url = url
        self.url_to_image = url_to_image
        self.published_at = published_at
        self.timestamp = time_utils.parse(self.published_at)

    def __str__(self):
        return "{} {} {} {}".format(self.timestamp, self.published_at, self.title, self.url)
