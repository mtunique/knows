from dbs import mongodb
from dbs import redisdb
import datetime
import hashlib
from knows.items import ArticleItem
import time
from bs4 import BeautifulSoup


class SpiderPipeline(object):
    @staticmethod
    def process_item(self, item, spider):
        return item


class ArticleInsertPipeline(object):
    @staticmethod
    def process_item(self, item, spider=None):
        tmp_item = dict(item)

        # If item['date'] is None, set it.
        #     eg:2014-03-23 22:33
        # set mongodb id
        #     hash link
        tmp_item.setdefault('date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        tmp_item.setdefault('_id', hashlib.md5(tmp_item['link']).hexdigest().upper())
        tmp_item.setdefault('time', str(int(time.time()*10000)))
        #time.sleep(0.001)

        img_list = BeautifulSoup(tmp_item['content']).find('img')
        if img_list:
            try:
                tmp_item.setdefault(img_list['src'])
            except IndexError:
                pass

        # link css href need to be reset according to the android device
        tmp_item['content'] = '<!DOCTYPE html><html><head><link rel="stylesheet" ' \
                              'href="file:///android_asset/mystyle.css"><meta ' \
                              'charset="utf-8"><script src="file:///android_asset/my.js"></script' \
                              '></head><body><div class="article_content" id="article_content">%s</div>' \
                              '<script type="text/javascript" src="file:///android_asset/myscript.js">' \
                              '</script></body></html>' % tmp_item['content']

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