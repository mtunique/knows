import mongodb

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleInsertPipline(object):
    def __init__(self):
        self.db = mongodb.db

    def process_item(self, item, spider):
        self.db.insert(dict(item))

