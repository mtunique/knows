import mongodb
import datetime
import hashlib

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleInsertPipline(object):
    def __init__(self):
        self.db = mongodb.db

    def process_item(self, item, spider):
        tmpItem = dict(item)

        # If item['date'] is None, set it.
        #     eg:2014-03-23 22:33
        # set mongodb id
        #     hash link
        tmpItem.setdefault('date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        tmpItem.setdefault('_id', hashlib.md5(tmpItem['link']).hexdigest().upper())

        #insert article information & content into db
        self.db.conntent.insert({'_id': tmpItem['_id'], 'content': tmpItem['content']})
        tmpItem.pop('content')
        self.db.article.insert(tmpItem)
        return item

