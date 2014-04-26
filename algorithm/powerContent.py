__author__ = 'mt'
# -*- coding: utf-8 -*-
from dbs import redisdb
from dbs import mongodb
from bs4 import BeautifulSoup


def to_string(content, strip=True):
    html = BeautifulSoup(content).html
    return html.get_text('\n', strip=strip)


if __name__ == '__main__':
    while True:
        tmp, content_hash = redisdb.db.brpop('content')
        content_html = mongodb.db.content.find_one({'_id': content_hash})['content']

        string = to_string(content_html)

        mongodb.db.s_content.update({'_id': content_hash},{'$set': {'s': string}}, upsert=True)
        redisdb.db.lpush('s_content', content_hash)