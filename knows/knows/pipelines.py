import DBs
import datetime
import hashlib
from knows.items import ArticleItem
import time

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleInsertPipline(object):
    def __init__(self):
        self.mongodb = DBs.db

    def process_item(self, item, spider=None):
        tmpItem = dict(item)

        # If item['date'] is None, set it.
        #     eg:2014-03-23 22:33
        # set mongodb id
        #     hash link
        tmpItem.setdefault('date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        tmpItem.setdefault('_id', hashlib.md5(tmpItem['link']).hexdigest().upper())
        tmpItem.setdefault('time', str(int(time.time()*10000)))
        time.sleep(0.001)

        tmpItem['content'] = '<!DOCTYPE html>\n<html>\n<head>\n<style>\nimg{\nmax-width:300px;\n}\n</style>\n</he' \
                             'ad>\n<body>\n'+tmpItem['content']+'</body>\n</html>'

        #insert article information & content into db
        self.mongodb.content.insert({'_id': tmpItem['_id'], 'content': tmpItem['content']})


        tmpItem.pop('content')
        self.mongodb.article.insert(tmpItem)
        return item

if __name__ == '__main__':
    a = ArticleInsertPipline()
    a.process_item(item=ArticleItem({'link':'dsadsad','content':'dasdasdassadsa'}))