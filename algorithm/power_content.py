__author__ = 'mt'
# -*- coding: utf-8 -*-
import sys
from dbs import redisdb
from dbs import mongodb
from bs4 import BeautifulSoup
from std_functions import doc_to_vector
from Bayes import bayes_text


def to_string(content, strip=True):
    return BeautifulSoup(content).html.body.get_text('\n', strip=strip)


def main():
    bs = bayes_text.NaiveBayesClassifier()
    bs.load_from_file()
    vocab = [i[:-1] for i in file('./dict_nostops.txt').readlines()]
    _vocab = dict()
    for word in vocab:
        _vocab[word] = len(_vocab)
    while True:
        tmp, content_hash = redisdb.db.brpop('content')

        content_html = mongodb.db.content.find_one({'_id': content_hash})['content']
        article = mongodb.db.article.find_one({'_id': content_hash})

        s = to_string(content_html)
        #print s
        #print article
        if article['tag'] not in ['viewdesign', 'uidesign', 'appanalyze']:
            tag = bs.bayes_classify(s)
            print tag
            mongodb.db.article.update({'_id': content_hash}, {'$set': {'tag': tag}}, upsert=True)
        #print content_hash

        time = mongodb.db.article.find_one({'_id': content_hash})['time']
        mongodb.db.s_content.update({'_id': content_hash}, {'$set': {'s': s, 'time': time}}, upsert=True)

        #TODO make article vector
        #print doc_to_vector(s, _vocab)

        #mongodb.db.v_content.update({'_id': content_hash}, {'$set': {'v': doc_to_vector(s, _vocab)}}, upsert=True)

        redisdb.db.lpush('s_content', content_hash)
        print 3
        break


if __name__ == '__main__':
    outfile = open('power.log', 'w')
    #sys.stderr = outfile
    #sys.stdout = outfile
    main()
    outfile.close()