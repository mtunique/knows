from dbs import mongodb
from dbs import redisdb
import datetime
import hashlib
from knows.items import ArticleItem
import time


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleInsertPipeline(object):
    def process_item(self, item, spider=None):
        tmp_item = dict(item)

        # If item['date'] is None, set it.
        #     eg:2014-03-23 22:33
        # set mongodb id
        #     hash link
        tmp_item.setdefault('date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        tmp_item.setdefault('_id', hashlib.md5(tmp_item['link']).hexdigest().upper())
        tmp_item.setdefault('time', str(int(time.time()*10000)))
        time.sleep(0.001)

        tmp_item['content'] = '<!DOCTYPE html>\n<html>\n<head>\n<script src="file:///android_asset/my.js" />\n' \
                              '</head>\n<body>\n'+tmp_item['content']+'</body>\n</html>'

        #insert article information & content into db
        mongodb.db.content.update({'_id': tmp_item['_id']},
                                  {'$set': {'content': tmp_item['content']}},
                                  upsert=True)
        redisdb.db.lpush('content', tmp_item['_id'])

        tmp_item.pop('content')
        mongodb.db.article.insert(tmp_item)
        #return item

if __name__ == '__main__':
    a = ArticleInsertPipeline()
    a.process_item(item=ArticleItem({'link':'dsadsad','content':'dasdasdassadsa'}))