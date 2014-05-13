__author__ = 'mt'
# -*- coding: utf-8 -*-
from dbs import redisdb
from dbs import mongodb
from bs4 import BeautifulSoup


def to_string(content, strip=True):
    return BeautifulSoup(content).html.body.get_text('\n', strip=strip)


def main():
    while True:
        tmp, content_hash = redisdb.db.brpop('content')
        try:
            content_html = mongodb.db.content.find_one({'_id': content_hash})['content']

            string = to_string(content_html)

            time = mongodb.db.article.find_one({'_id': content_hash})['time']
            mongodb.db.s_content.update({'_id': content_hash}, {'$set': {'s': string, 'time': time}}, upsert=True)
            redisdb.db.lpush('s_content', content_hash)
        except Exception as err:
            print '[%s] %s' % (content_hash, err.message)

if __name__ == '__main__':
    main()