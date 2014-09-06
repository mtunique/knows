__author__ = 'mt'
# -*- coding: utf-8 -*-
import sys
import traceback
from dbs import redisdb, mongodb
from std_functions import to_string, doc_to_vector, vector_to_topic_vector, get_base_vectors
from Bayes import bayes_text


def main():
    bs = bayes_text.NaiveBayesClassifier()
    base_vectors = get_base_vectors(mongodb.db)
    bs.load_from_file()
    vocab = [i[:-1] for i in file('./dict_nostops.txt').readlines()]
    _vocab = dict()
    for word in vocab:
        _vocab[word] = len(_vocab)
    while True:
        tmp, content_hash = redisdb.db.brpop('content')
        try:
            content_html = mongodb.db.content.find_one({'_id': content_hash})['content']
            article = mongodb.db.article.find_one({'_id': content_hash})

            s = to_string(content_html)
            #print s
            #print article
            if article['tag'] not in ['viewdesign', 'uidesign', 'appanalyze']:
                tag = bs.bayes_classify(s)
                #print tag
                mongodb.db.article.update({'_id': content_hash}, {'$set': {'tag': tag}}, upsert=True)
            #print content_hash

            time = mongodb.db.article.find_one({'_id': content_hash})['time']
            mongodb.db.s_content.update({'_id': content_hash}, {'$set': {'s': s, 'time': time}}, upsert=True)

            #print doc_to_vector(s, _vocab)
            t = vector_to_topic_vector(doc_to_vector(s, _vocab), base_vectors)
            mongodb.db.v_content.update({'_id': content_hash},
                                        {'$set': {'t': t}},
                                        upsert=True)

            redisdb.db.lpush('s_content', content_hash)
        except Exception as err:
            print '[%s]:%s' % (content_hash, str(err.message))
            traceback.print_exc()
            redisdb.db.lpush('power_error_content', content_hash)
        #print 3
        #break


if __name__ == '__main__':
    outfile = open('power.log', 'w')
    sys.stderr = outfile
    sys.stdout = outfile
    main()
    outfile.close()