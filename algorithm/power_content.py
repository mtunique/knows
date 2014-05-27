__author__ = 'mt'
# -*- coding: utf-8 -*-
import sys
from dbs import redisdb
from dbs import mongodb
from bs4 import BeautifulSoup
from std_functions import doc_to_vector


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
            mongodb.db.v_content.update({'_id': content_hash}, {'$set': {'v': doc_to_vector(string)}}, upsert=True)
            redisdb.db.lpush('s_content', content_hash)
        except Exception as err:
            print '[%s] %s' % (content_hash, str(err.args))

if __name__ == '__main__':
    outfile = open('power.log', 'w')
    sys.stderr = outfile
    sys.stdout = outfile
    main()